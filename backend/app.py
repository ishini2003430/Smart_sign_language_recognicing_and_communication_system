import sys
import os
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Add scripts directory to system path to import evaluation logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.compare_gestures import evaluate_learner_sign

app = FastAPI(title="Smart SLSL Correctness & Feedback API")

# Enable Cross-Origin Resource Sharing (CORS) for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluationRequest(BaseModel):
    sign_id: str
    landmarks: List[List[float]]  # Array of frame landmark vectors [(T, 225)]

@app.get("/")
def home():
    return {"status": "Smart SLSL Backend Running"}

@app.post("/api/evaluate-sign")
def evaluate_sign(payload: EvaluationRequest):
    try:
        learner_seq = np.array(payload.landmarks)
        if learner_seq.size == 0:
            raise HTTPException(status_code=400, detail="Empty landmark sequence provided.")

        result = evaluate_learner_sign(learner_seq, payload.sign_id)
        return {"success": True, "data": result}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")