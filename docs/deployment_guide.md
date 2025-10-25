# MinutesAI 웹 배포 가이드

## 📋 배포 옵션 비교

| 옵션 | 난이도 | 비용 | 속도 | 권장 용도 |
|------|--------|------|------|----------|
| **Gradio Share** | ⭐ 매우 쉬움 | 무료 | 느림 | 테스트, 데모 |
| **Hugging Face Spaces** | ⭐⭐ 쉬움 | 무료/유료 | 중간 | 소규모 서비스 |
| **Docker (자체 서버)** | ⭐⭐⭐ 중간 | 서버 비용 | 빠름 | 프로덕션 |
| **클라우드 (AWS/GCP)** | ⭐⭐⭐⭐ 어려움 | 고비용 | 매우 빠름 | 대규모 서비스 |

---

## 1️⃣ Gradio Share (임시 공개 링크)

### 사용 방법
```python
# src/gradio_app.py의 마지막 부분 수정
demo.launch(
    share=True,  # False → True로 변경
    show_error=True
)
```

### 실행
```bash
cd src
python3 gradio_app.py
```

### 결과
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxx.gradio.live
```

### 장점
- ✅ 설정 불필요
- ✅ 완전 무료
- ✅ 즉시 사용 가능

### 단점
- ❌ 72시간 후 링크 만료
- ❌ 본인 PC가 켜져있어야 함
- ❌ 본인 PC의 성능에 의존
- ❌ 프로덕션 부적합

### 사용 시나리오
- 친구에게 빠르게 공유
- 짧은 데모/발표
- 테스트용

---

## 2️⃣ Hugging Face Spaces (권장)

### 특징
- 완전 무료 (CPU 기본)
- 24/7 운영
- 자동 배포
- Gradio 네이티브 지원

### 배포 단계

#### Step 1: 계정 생성
https://huggingface.co/join

#### Step 2: New Space 생성
1. https://huggingface.co/spaces → "Create new Space"
2. 설정:
   - **Space name**: minutesai
   - **SDK**: Gradio
   - **Hardware**: CPU basic (무료)

#### Step 3: 파일 업로드
업로드할 파일:
- `deployment/huggingface/app.py`
- `deployment/huggingface/requirements.txt`

**Git 방식 (권장):**
```bash
# Space 클론
git clone https://huggingface.co/spaces/YOUR_USERNAME/minutesai
cd minutesai

# 파일 복사
cp deployment/huggingface/app.py .
cp deployment/huggingface/requirements.txt .

# 커밋 및 푸시
git add .
git commit -m "Initial deployment"
git push
```

**웹 인터페이스:**
- Space의 "Files" 탭
- "Add file" → "Upload files"
- 파일 드래그 앤 드롭

#### Step 4: 자동 빌드
- 5-10분 대기
- 빌드 로그 확인 가능

#### Step 5: 접속
```
https://huggingface.co/spaces/YOUR_USERNAME/minutesai
```

### 무료 vs 유료

| | 무료 (CPU) | 유료 (GPU T4) |
|---|------------|---------------|
| **가격** | $0 | $0.60/시간 (~$432/월) |
| **모델** | tiny, base, small | 모든 모델 |
| **속도** | 1분 음성 = 2-3분 | 1분 음성 = 10-30초 |
| **메모리** | 16GB | 16GB + GPU |
| **권장 사용** | 개인/소규모 | 비즈니스 |

### GPU 업그레이드 방법
1. Space 설정 → "Settings"
2. "Space hardware" → "NVIDIA T4 small" 선택
3. 과금 시작됨 (시간당)

### 장점
- ✅ 완전 무료 옵션
- ✅ 24/7 자동 운영
- ✅ 배포 자동화
- ✅ 관리 불필요

### 단점
- ❌ CPU는 느림
- ❌ GPU는 비용 발생
- ❌ 동시 사용자 제한
- ❌ 커스터마이징 제한

### 사용 시나리오
- 개인 프로젝트
- 포트폴리오
- 소규모 팀 내부용
- MVP 테스트

---

## 3️⃣ Docker (자체 서버)

### 사전 준비
- Docker 설치
- 서버 또는 클라우드 VM
- 최소 4GB RAM (8GB 권장)

### 배포 단계

#### Step 1: Docker 빌드
```bash
cd /Users/gimseonghun/Project/minutesAI

# 이미지 빌드
docker build -t minutesai .
```

#### Step 2: Docker 실행
```bash
# 기본 실행
docker run -p 7860:7860 minutesai

# 또는 docker-compose 사용 (권장)
docker-compose up -d
```

#### Step 3: 접속
```
http://서버_IP:7860
```

### Docker Compose 사용 (권장)
```bash
# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down

# 재시작
docker-compose restart
```

### 장점
- ✅ 완전한 제어권
- ✅ 높은 성능 (서버 성능에 따라)
- ✅ 프라이빗 배포
- ✅ 커스터마이징 자유

### 단점
- ❌ 서버 관리 필요
- ❌ 보안 설정 필요
- ❌ 비용 (서버)
- ❌ 기술적 난이도

### 클라우드 배포 예시

#### AWS EC2
```bash
# t3.medium 이상 권장 (2 vCPU, 4GB RAM)
# 1. EC2 인스턴스 생성
# 2. Docker 설치
# 3. 코드 클론
git clone https://github.com/YOUR_REPO/minutesAI.git
cd minutesAI

# 4. Docker Compose 실행
docker-compose up -d

# 5. 포트 7860 열기 (Security Group)
```

#### Google Cloud Run (서버리스)
```bash
# 1. gcloud CLI 설치
# 2. 프로젝트 생성
gcloud config set project YOUR_PROJECT_ID

# 3. 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/minutesai

# 4. Cloud Run 배포
gcloud run deploy minutesai \
  --image gcr.io/YOUR_PROJECT_ID/minutesai \
  --platform managed \
  --region asia-northeast3 \
  --memory 4Gi \
  --port 7860 \
  --allow-unauthenticated
```

### 비용 예상 (월별)

| 플랫폼 | 스펙 | 예상 비용 |
|--------|------|-----------|
| **AWS EC2 (t3.medium)** | 2 vCPU, 4GB | ~$30/월 |
| **GCP Compute (e2-medium)** | 2 vCPU, 4GB | ~$25/월 |
| **Digital Ocean Droplet** | 2 vCPU, 4GB | $24/월 |
| **AWS EC2 GPU (g4dn.xlarge)** | 4 vCPU, 16GB, T4 GPU | ~$400/월 |

---

## 4️⃣ 클라우드 관리형 서비스

### AWS SageMaker / GCP Vertex AI
- 프로덕션급 ML 인프라
- 오토스케일링
- 고비용 (월 $500+)
- 기업용

### Render / Railway / Fly.io
- 간단한 배포
- 무료 티어 있음
- Docker 지원
- Dockerfile만 있으면 배포 가능

---

## 🎯 추천 배포 전략

### 개인 프로젝트 / 포트폴리오
→ **Hugging Face Spaces (무료 CPU)**

### 소규모 팀 / 스타트업
→ **Hugging Face Spaces (GPU)** 또는 **Docker on 저렴한 클라우드**

### 중규모 서비스 (일 100명 이상)
→ **Docker on AWS/GCP** + 로드 밸런서

### 대규모 서비스
→ **Kubernetes** + **관리형 ML 서비스**

---

## 🔐 보안 고려사항

### 인증 추가
Gradio는 기본 인증을 지원합니다:

```python
demo.launch(
    auth=("username", "password")  # 간단한 인증
)
```

### HTTPS 설정
- Hugging Face Spaces: 자동 HTTPS
- Docker: nginx + Let's Encrypt 사용

### 파일 업로드 제한
```python
# 파일 크기 제한 (예: 100MB)
audio_input = gr.Audio(
    type="filepath",
    max_length=600  # 최대 10분
)
```

---

## 📊 성능 최적화

### 모델 선택
- **tiny/base**: 빠르지만 부정확
- **small**: 균형잡힌 선택 (권장)
- **medium/large**: 정확하지만 느림 (GPU 필요)

### 캐싱
- Docker volume으로 모델 캐시 저장
- 재시작 시 다운로드 방지

### 동시 처리
- 큐잉 시스템 추가
- 여러 워커 프로세스

---

## 🆘 문제 해결

### 메모리 부족
```bash
# Docker 메모리 증가
docker run -m 8g -p 7860:7860 minutesai
```

### 느린 처리 속도
- GPU 사용
- 더 작은 모델 사용
- 파일 길이 제한

### 모델 다운로드 실패
- SSL 인증서 설정 확인
- 인터넷 연결 확인
- 수동으로 모델 다운로드

---

## 📚 추가 자료

- [Gradio 공식 문서](https://gradio.app/docs/)
- [Hugging Face Spaces 가이드](https://huggingface.co/docs/hub/spaces)
- [Docker 공식 문서](https://docs.docker.com/)
- [Whisper GitHub](https://github.com/openai/whisper)
