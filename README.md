# 😴 하품/음성 피로도 감지 모델 API
오디오 파일을 입력받아 **하품(yawn)** 및 **졸림(sleepy)** 여부를 예측하는 FastAPI 기반의 서버


## 📁 프로젝트 구조

```
├── main.py # FastAPI 서버 엔트리포인트
├── .gitattributes # Git LFS 설정
├── sleepy_project/
│ ├── model/sleepy_v1/ # 졸림 감지 모델
│ │ ├── config.json
│ │ └── model.safetensors
│ ├── scripts/inference.py # sleepy 예측 스크립트
│ └── requirements.txt
├── yawn_project/
│ ├── model/yawn_AST/ # 하품 감지 모델
│ │ ├── config.json
│ │ ├── model.safetensors
│ │ └── preprocessor_config.json
│ ├── scripts/inference.py # yawn 예측 스크립트
│ └── requirements.txt
├── utils/
│ └── audio_utils.py # 공통 오디오 전처리 유틸
```

## 🚀 실행 환경

### 1. Python
- Python 3.8 이상 권장

### 2. 필수 패키지
`requirements.txt` 파일에 명시된 패키지를 설치하여 실행 환경 설정
```bash
pip install -r requirements.txt
```
### 3. 추가 설치
- FFmpeg: 오디오 변환을 위해 필요. 설치 후 `ffmpeg` 명령어가 시스템 경로(PATH)에 포함되어야 함

- Git LFS: `safetensors` 모델 파일 다운로드 및 로딩 
```bash
git lfs install
git lfs pull
```

## ⚙️ 실행 방법
### FastAPI 서버 실행 (로컬 테스트용)
```bash
# 방법 1
uvicorn main:app --reload

# 방법 2
python -m uvicorn main:app --reload
```

## 🎯 API 사용법
### ▶️ POST /predict
- 오디오 파일 업로드 → 졸림/하품 여부 반환
- 요청 형식: multipart/form-data
- 파일 필드명: file
- 지원 포맷: audio/m4a (기타 오디오 형식도 지원되나, 내부적으로 `.m4a`만을 `.wav`로 변환하여 처리)

✅ 예시 응답
```
{
  "yawn": true,
  "sleepy": false
}
```

## ⚠️ 주의 사항
- `.safetensors` 모델 파일은 Git LFS로 관리되며, `git lfs pull` 을 하지 않으면 로딩에 실패할 수 있음.
- m4a → wav 변환을 위해 ffmpeg가 반드시 설치되어야 함.
- Windows에서는 `AudioSegment.converter` 경로를 명시적으로 지정해야 할 수 있음.
