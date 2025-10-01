import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 로드
load_dotenv()

# # 환경변수에서 API_KEY 가져오기
# api_key = os.getenv("API_KEY")
# print("")  # 앞 5자리만 찍어서 확인

# # OpenAI 클라이언트 생성
# client = OpenAI(api_key=api_key)
# print("클라이언트 준비 완료")


response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text);
print("end");
