import React, { useRef, useState, useEffect } from 'react';
import { FilesetResolver, PoseLandmarker, HandLandmarker } from '@mediapipe/tasks-vision';
import axios from 'axios';

const SignEvaluator = ({ currentSignId = 'S01_amma' }) => {
  const videoRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedLandmarks, setRecordedLandmarks] = useState([]);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detectorsReady, setDetectorsReady] = useState(false);

  const poseDetectorRef = useRef(null);
  const handDetectorRef = useRef(null);
  const animationFrameRef = useRef(null);
  const startTimeRef = useRef(null);

  // 1. Initialize MediaPipe Detectors
  useEffect(() => {
    const initDetectors = async () => {
      const vision = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm'
      );

      poseDetectorRef.current = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task',
          delegate: 'GPU'
        },
        runningMode: 'VIDEO',
        numPoses: 1
      });

      handDetectorRef.current = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
          delegate: 'GPU'
        },
        runningMode: 'VIDEO',
        numHands: 2
      });

      setDetectorsReady(true);
    };

    initDetectors();
  }, []);

  // 2. Start Webcam Stream
  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => console.error('Webcam Access Error:', err));
  }, []);

  // 3. Process Video Frames and Capture Landmarks
  const processFrame = () => {
    if (
      videoRef.current &&
      videoRef.current.readyState >= 2 &&
      poseDetectorRef.current &&
      handDetectorRef.current
    ) {
      const now = performance.now();
      if (!startTimeRef.current) startTimeRef.current = now;
      const timestampMs = Math.round(now - startTimeRef.current);

      // Extract Pose
      const poseResults = poseDetectorRef.current.detectForVideo(videoRef.current, timestampMs);
      let poseVec = new Array(33 * 3).fill(0);
      if (poseResults.poseLandmarks && poseResults.poseLandmarks.length > 0) {
        poseVec = poseResults.poseLandmarks[0].flatMap((lm) => [lm.x, lm.y, lm.z]);
      }

      // Extract Hands
      const handResults = handDetectorRef.current.detectForVideo(videoRef.current, timestampMs);
      let lhVec = new Array(21 * 3).fill(0);
      let rhVec = new Array(21 * 3).fill(0);

      if (handResults.landmarks && handResults.handedness) {
        handResults.landmarks.forEach((landmarks, idx) => {
          const label = handResults.handedness[idx][0].categoryName;
          const coords = landmarks.flatMap((lm) => [lm.x, lm.y, lm.z]);
          if (label === 'Left') lhVec = coords;
          if (label === 'Right') rhVec = coords;
        });
      }

      // Concatenate to 225 features: [Left Hand (63), Right Hand (63), Pose (99)]
      const frameFeatures = [...lhVec, ...rhVec, ...poseVec];

      setRecordedLandmarks((prev) => [...prev, frameFeatures]);
    }

    if (isRecording) {
      animationFrameRef.current = requestAnimationFrame(processFrame);
    }
  };

  // 4. Start / Stop Recording
  const handleStartRecording = () => {
    setRecordedLandmarks([]);
    setEvaluation(null);
    startTimeRef.current = performance.now();
    setIsRecording(true);
  };

  useEffect(() => {
    if (isRecording) {
      animationFrameRef.current = requestAnimationFrame(processFrame);
    } else if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    return () => cancelAnimationFrame(animationFrameRef.current);
  }, [isRecording]);

  const handleStopRecording = () => {
    setIsRecording(false);
  };

  // 5. Send Extracted Sequence to FastAPI Backend
  const handleEvaluate = async () => {
    if (!recordedLandmarks.length) return;

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/evaluate-sign', {
        sign_id: currentSignId,
        landmarks: recordedLandmarks
      });
      setEvaluation(response.data.data);
    } catch (error) {
      console.error('API Evaluation Error:', error);
      alert('Failed to evaluate sign. Ensure backend server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-lg border">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
        Sign Correctness Evaluator
      </h2>

      {/* Video Feed */}
      <div className="relative rounded-lg overflow-hidden bg-black aspect-video mb-4">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-cover transform -scale-x-100"
        />
        {!detectorsReady && (
          <div className="absolute inset-0 bg-black/70 flex items-center justify-center text-white">
            Loading MediaPipe AI Models...
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="flex justify-center gap-4 mb-6">
        {!isRecording ? (
          <button
            onClick={handleStartRecording}
            disabled={!detectorsReady}
            className="px-6 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            Start Gesture
          </button>
        ) : (
          <button
            onClick={handleStopRecording}
            className="px-6 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 animate-pulse"
          >
            Stop Gesture ({recordedLandmarks.length} frames)
          </button>
        )}

        <button
          onClick={handleEvaluate}
          disabled={loading || isRecording || !recordedLandmarks.length}
          className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Evaluating...' : 'Submit & Evaluate'}
        </button>
      </div>

      {/* Results Display */}
      {evaluation && (
        <div className="p-5 bg-gray-50 rounded-lg border border-gray-200">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-lg font-bold text-gray-800">Evaluation Result</h3>
            <span
              className={`text-xl font-black ${
                evaluation.is_correct ? 'text-green-600' : 'text-red-600'
              }`}
            >
              {evaluation.correctness_score}%
            </span>
          </div>

          <p className="text-sm text-gray-600 mb-3">
            Matched Reference: <span className="font-semibold">{evaluation.matched_expert}</span>
          </p>

          <div className="space-y-2 border-t pt-3">
            <p className="text-gray-800">
              <strong className="text-blue-900">🇬🇧 English:</strong> {evaluation.feedback.en}
            </p>
            <p className="text-gray-800">
              <strong className="text-blue-900">🇱🇰 සිංහල:</strong> {evaluation.feedback.si}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SignEvaluator;