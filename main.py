from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os

from utils.audio_utils import convert_m4a_to_wav
from yawn_project.scripts.inference import predict_yawn
from sleepy_project.scripts.inference import predict_sleepiness

app = FastAPI()

# API endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio"):
        return JSONResponse(content={"error": "Only audio files are supported."}, status_code=400)

    try:
        contents = await file.read()
        wav_path = convert_m4a_to_wav(contents)

        yawn = predict_yawn(wav_path)
        sleepy = predict_sleepiness(wav_path)

        os.remove(wav_path)

        return {"yawn": yawn, "sleepy": sleepy}

    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)