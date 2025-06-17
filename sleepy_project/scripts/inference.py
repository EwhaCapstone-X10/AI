import torch
import torchaudio
from transformers import AutoModelForAudioClassification, Wav2Vec2FeatureExtractor
import os

# (global) model loading
sleepy_model = AutoModelForAudioClassification.from_pretrained("minjeon99/sleepy-model-bin")
sleepy_fe = Wav2Vec2FeatureExtractor.from_pretrained("superb/wav2vec2-base-superb-er")
sleepy_model.eval()

# preprocess function
def preprocess_audio(path: str, target_sr: int = 16000):
    speech, sr = torchaudio.load(path)
    if sr != target_sr:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)
        speech = resampler(speech)

    if speech.ndim > 1 and speech.shape[0] > 1:
        speech = speech.mean(dim=0)

    inputs = sleepy_fe(
        speech,
        sampling_rate=target_sr,
        return_tensors="pt",
        padding="longest",
        truncation=True,
        max_length=16000
    )
    return inputs

# inference function
def predict_sleepiness(audio_path: str) -> dict:
    inputs = preprocess_audio(audio_path)
    with torch.no_grad():
        logits = sleepy_model(**inputs).logits
        predicted = torch.argmax(logits, dim=-1).item()
    return bool(predicted)

# CLI test
if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    result = predict_sleepiness(path)
    print(f"✅ Prediction: {result}")
