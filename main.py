import os
from dotenv import load_dotenv

import whisper
from openai import OpenAI
import shutil

load_dotenv() # .env 파일 로드
api_key = os.getenv("API_KEY") # 환경변수에서 API_KEY 가져오기

print("Whisper 모델 불러오는 중... (처음이면 다운로드 시간이 걸릴 수 있어요)")
model = whisper.load_model("small") # 모델 로드 (tiny, base, small, medium, large 중 선택)
print("모델 로드 완료!")


# 음성 파일 변환
result = model.transcribe("test_audio/test01.m4a")

print(result["text"])

print("종료")