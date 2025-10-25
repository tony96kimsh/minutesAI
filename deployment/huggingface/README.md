# MinutesAI Hugging Face Spaces 배포 가이드

## 🚀 배포 단계

### 1. Hugging Face 계정 생성
https://huggingface.co/join 에서 무료 계정 생성

### 2. New Space 생성
1. https://huggingface.co/spaces 접속
2. "Create new Space" 클릭
3. 설정:
   - **Space name**: minutesai (원하는 이름)
   - **License**: MIT
   - **Select the Space SDK**: Gradio
   - **Space hardware**: CPU basic (무료)

### 3. 파일 업로드

Space가 생성되면 다음 파일들을 업로드:

```
your-space/
├── app.py              (이 폴더의 app.py)
└── requirements.txt    (이 폴더의 requirements.txt)
```

**방법 1: 웹 인터페이스**
- "Files" 탭에서 "Add file" → "Upload files" 클릭
- `app.py`와 `requirements.txt` 드래그 앤 드롭

**방법 2: Git (추천)**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/minutesai
cd minutesai
cp ../deployment/huggingface/app.py .
cp ../deployment/huggingface/requirements.txt .
git add .
git commit -m "Initial deployment"
git push
```

### 4. 자동 빌드 및 배포

파일을 업로드하면 자동으로:
1. 의존성 패키지 설치
2. 앱 빌드
3. 배포 완료

약 5-10분 소요됩니다.

### 5. 접속

배포 완료 후:
```
https://huggingface.co/spaces/YOUR_USERNAME/minutesai
```

## ⚙️ 업그레이드 옵션

### GPU 사용 (유료)

더 빠른 처리를 원한다면:
1. Space 설정에서 "Settings" 클릭
2. "Space hardware" → "NVIDIA T4" 선택 ($0.60/시간)
3. `app.py`에서 모델을 "medium" 또는 "large"로 변경 가능

## 📊 무료 vs 유료 비교

| 기능 | 무료 (CPU) | 유료 (GPU T4) |
|------|-----------|--------------|
| 가격 | $0 | $0.60/시간 |
| 모델 | tiny, base, small | 모든 모델 |
| 처리 속도 | 느림 (1분 음성 = 2-3분) | 빠름 (1분 음성 = 10-30초) |
| 동시 사용자 | 제한적 | 더 많음 |

## 🔒 보안 고려사항

- 업로드된 파일은 서버에 임시 저장됨
- 민감한 정보가 포함된 파일은 주의
- Private Space로 설정 가능 (설정에서 변경)

## 📝 참고 링크

- [Gradio Spaces 문서](https://huggingface.co/docs/hub/spaces-sdks-gradio)
- [Space 예제들](https://huggingface.co/spaces)
