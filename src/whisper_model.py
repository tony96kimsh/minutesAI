# WhisperModel.py
import ssl
import certifi
import whisper

# SSL 인증서 문제 해결
ssl._create_default_https_context = ssl._create_unverified_context

def load_whisper_model(model_size="small"):
    print("Whisper 모델 불러오는 중... (처음이면 다운로드 시간이 걸릴 수 있어요)")
    model = whisper.load_model(model_size)
    print("모델 로드 완료!")
    return model

def transcribe_audio(model, audio_path):
    result = model.transcribe(audio_path)
    return result["text"]
