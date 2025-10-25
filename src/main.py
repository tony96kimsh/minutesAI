# main.py
import whisper_model
import FileHelper

# 오디오 탐색기 호출
path = FileHelper.select_audio()

if path != None:
    # Whisper 모델 불러오기
    model = whisper_model.load_whisper_model("small")
    # 음성 파일 변환
    stt_text = whisper_model.transcribe_audio(model, path)

    print("변환 텍스트: ", stt_text)
else:
    print("경로 선택이 취소되었습니다.")



