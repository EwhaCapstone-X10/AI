import os
import torch
import librosa
from transformers import ASTFeatureExtractor, ASTForAudioClassification

# (global) model loading
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "yawn_AST"))

print("📦 모델 로드 중")
yawn_model = ASTForAudioClassification.from_pretrained("minjeon99/yawn-ast-bin")
yawn_fe = ASTFeatureExtractor.from_pretrained(MODEL_PATH)
print("✅ 모델 로딩 완료")
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
