
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from src.translation.app import translate_signs
from src.translation.translation_pipeline import translate_topk_sequence


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend" / "translation-pp1"

app = Flask(__name__)


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/assets/<path:filename>")
def frontend_assets(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.post("/api/translate")
def translate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "ERROR",
            "message": "Please provide a valid JSON request."
        }), 400

    mode = data.get("mode")

    try:
        if mode == "direct":
            glosses = data.get("glosses")

            if (
                not isinstance(glosses, list)
                or not glosses
                or not all(
                    isinstance(word, str) and word.strip()
                    for word in glosses
                )
            ):
                return jsonify({
                    "status": "ERROR",
                    "message": "Please provide a list of sign glosses."
                }), 400

            result = translate_signs(glosses)

            if result["pattern"] == "UNKNOWN":
                return jsonify({
                    "status": "UNSUPPORTED_PATTERN",
                    "english": None,
                    "sinhala": None,
                    "pattern": "UNKNOWN",
                    "message": "This sentence pattern is not yet supported."
                })

            return jsonify({
                "status": "SUCCESS",
                **result
            })

        elif mode == "topk":
            sequence = data.get("sequence")

            if not isinstance(sequence, list) or not sequence:
                return jsonify({
                    "status": "ERROR",
                    "message": "Please provide a Top-K sequence."
                }), 400

            for position in sequence:
                if not isinstance(position, dict):
                    raise ValueError(
                        "Each position must be an object."
                    )

                candidates = position.get("top_k")

                if not isinstance(candidates, list) or not candidates:
                    raise ValueError(
                        "Every position needs at least one candidate."
                    )

                for candidate in candidates:
                    if not isinstance(candidate, dict):
                        raise ValueError("Invalid candidate.")

                    gloss = candidate.get("gloss")
                    score = candidate.get("score")

                    if not isinstance(gloss, str) or not gloss.strip():
                        raise ValueError("Invalid candidate gloss.")

                    if (
                        isinstance(score, bool)
                        or not isinstance(score, (int, float))
                        or not 0 <= score <= 1
                    ):
                        raise ValueError(
                            "Scores must be numeric values from 0 to 1."
                        )

            result = translate_topk_sequence(sequence)

            return jsonify(result)

        return jsonify({
            "status": "ERROR",
            "message": "Unsupported translation mode."
        }), 400

    except (ValueError, TypeError, KeyError) as error:
        return jsonify({
            "status": "ERROR",
            "message": str(error)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
