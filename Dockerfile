# MinutesAI Dockerfile

FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (ffmpeg는 Whisper에 필요)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY src/ ./src/

# 작업 디렉토리를 src로 변경
WORKDIR /app/src

# 포트 노출
EXPOSE 7860

# 환경 변수 설정
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# 앱 실행
CMD ["python3", "gradio_app.py"]
