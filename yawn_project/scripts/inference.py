import os
import torch
import librosa
from transformers import ASTFeatureExtractor, ASTForAudioClassification

# (global) model loading
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "yawn_AST_bin"))

yawn_model = ASTForAudioClassification.from_pretrained(MODEL_PATH, use_safetensors=False)
yawn_fe = ASTFeatureExtractor.from_pretrained(MODEL_PATH)
yawn_model.eval()

# preprocess function
def predict_yawn(wav_path):
    waveform, sample_rate = librosa.load(wav_path, sr=16000)
    waveform = torch.tensor(waveform).squeeze()

    inputs = yawn_fe(waveform, sampling_rate=sample_rate, return_tensors="pt")

    with torch.no_grad():
        outputs = yawn_model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probs, dim=-1).item()

    return bool(predicted_class)
