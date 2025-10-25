# AI Minutes
개발 순서

1. FileIO - 음성파일 input
2. STT (Whisper)
    
    [STT를 통한 텍스트 파일 추출](https://www.notion.so/STT-26ef398452c380faa390d3af77f5b0a5?pvs=21)
    
3. LLM을 통한 정리(Gemma)
    
    [텍스트 파일 LLM 전송](https://www.notion.so/LLM-26ef398452c3803cabd0dd19c4d66847?pvs=21)
    
4. output
5. UI 구현
    - https://streamlit.io/
    - https://www.gradio.app/
6. FastAPI 클라이언트 서버 연결

사용자 로직

1. 환경 선택 (웹, 로컬)
2. 음성 파일 추가 및 부가 설명
3. 챗봇을 통한 답변 
4. 추가 질문 전달 및 답변





단순한 형태의 whisper 로컬을 통한 STT
```
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
```