# 🎙️ MinutesAI

AI 기반 음성/영상 파일 자동 텍스트 변환 서비스

OpenAI Whisper를 사용하여 회의록, 강의, 인터뷰 등의 음성을 텍스트로 자동 변환합니다.

[![Hugging Face Space](https://img.shields.io/badge/🤗-Hugging%20Face-yellow)](https://huggingface.co/spaces/AmoryKim/minutesAI)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ 주요 기능

- 🎯 **자동 음성 인식(STT)** - Whisper AI 모델 사용
- 🌐 **웹 UI** - 직관적인 Gradio 인터페이스
- 📝 **텍스트 편집** - 변환된 텍스트 실시간 수정 가능
- 💾 **파일 저장** - 텍스트를 .txt 파일로 저장
- ⚙️ **모델 선택** - tiny, base, small, medium, large 중 선택
- 📊 **진행 상황 표시** - 프로그레스 바와 토스트 알림

---

## 🚀 사용 방법

### 옵션 1: 웹에서 바로 사용 (추천)

**설치 불필요! 브라우저에서 바로 사용하세요:**

👉 **https://huggingface.co/spaces/AmoryKim/minutesAI**

1. 링크 접속
2. 파일 업로드
3. 변환하기 클릭
4. 완료!

---

### 옵션 2: 로컬 실행 (개발자용)

#### 사전 준비
- Python 3.11 이상
- 4GB 이상 RAM (8GB 권장)

#### 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/YOUR_USERNAME/minutesAI.git
cd minutesAI

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 웹 UI 실행
cd src
python3 gradio_app.py
```

브라우저가 자동으로 열리고 `http://localhost:7860` 접속

#### CLI 버전 (간단 테스트)

```bash
cd src
python3 main.py
```

---

### 옵션 3: 데스크톱 앱 (오프라인 사용)

#### macOS 빌드 및 실행

```bash
# 1. PyInstaller 설치
pip install pyinstaller

# 2. 빌드 실행
./build.sh

# 3. 실행
open dist/MinutesAI.app
```

자세한 내용은 [`docs/desktop_app_guide.md`](docs/desktop_app_guide.md) 참고

---

## 📋 지원 형식

**오디오:** WAV, MP3, M4A, FLAC, OGG, OPUS
**영상:** MP4, MKV, MOV, AVI, WEBM

---

## 🎯 Whisper 모델 선택 가이드

| 모델 | 크기 | 메모리 | 속도 | 정확도 | 권장 용도 |
|------|------|--------|------|--------|----------|
| **tiny** | ~75MB | ~1GB | 매우 빠름 | 낮음 | 빠른 테스트 |
| **base** | ~150MB | ~1GB | 빠름 | 보통 | 일반 사용 |
| **small** | ~500MB | ~2GB | 중간 | 좋음 | **권장** |
| **medium** | ~1.5GB | ~5GB | 느림 | 매우 좋음 | 고품질 필요 시 |
| **large** | ~3GB | ~10GB | 매우 느림 | 최고 | 최고 품질 필요 시 |

**⚠️ 첫 실행 시 모델 다운로드로 시간이 소요됩니다. (1-5분)**

---

## 🛠️ 기술 스택

- **STT 엔진**: [OpenAI Whisper](https://github.com/openai/whisper)
- **웹 프레임워크**: [Gradio](https://gradio.app/)
- **딥러닝**: PyTorch
- **언어**: Python 3.11+

---

## 📂 프로젝트 구조

```
minutesAI/
├── src/
│   ├── gradio_app.py        # Gradio 웹 UI (메인)
│   ├── main.py              # CLI 버전
│   ├── whisper_model.py     # Whisper 모델 래퍼
│   ├── FileHelper.py        # 파일 선택 유틸리티
│   └── llm_model.py         # LLM 통합 (TODO)
├── deployment/
│   └── huggingface/         # HF Spaces 배포 파일
├── docs/                    # 문서
├── requirements.txt         # Python 의존성
├── build.spec              # PyInstaller 빌드 설정
├── build.sh                # 빌드 스크립트
└── README.md               # 이 파일
```

---

## 🚢 배포 옵션

### 1. Hugging Face Spaces (현재 배포됨 ✅)
- **URL**: https://huggingface.co/spaces/AmoryKim/minutesAI
- 무료 호스팅
- 24/7 운영

### 2. 데스크톱 앱 (로컬 빌드)
- 실행 파일로 배포
- 오프라인 사용 가능
- 완전한 프라이버시

### 3. Docker (자체 서버)
```bash
docker-compose up -d
```

자세한 배포 가이드: [`docs/deployment_guide.md`](docs/deployment_guide.md)

---

## 📖 문서

- [Gradio 사용 가이드](docs/gradio_usage.md)
- [배포 가이드](docs/deployment_guide.md)
- [데스크톱 앱 빌드](docs/desktop_app_guide.md)
- [Whisper Web 가이드](docs/whisper_web_guide.md)

---

## 🔒 프라이버시

- **로컬 실행**: 모든 처리가 사용자 PC에서 이루어집니다
- **웹 버전**: Hugging Face 서버에서 처리됩니다
- **데이터 보관**: 임시 처리 후 자동 삭제
- **민감 정보**: .env 파일로 관리 (Git 제외)

---

## 🙏 감사의 말

- [OpenAI Whisper](https://github.com/openai/whisper) - STT 엔진
- [Gradio](https://gradio.app/) - 웹 UI 프레임워크
- [Hugging Face](https://huggingface.co/) - 무료 호스팅

---

Made with ❤️ by AmoryKim
