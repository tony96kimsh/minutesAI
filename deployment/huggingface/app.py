"""
MinutesAI - Hugging Face Spaces용 배포 파일
"""

import gradio as gr
import whisper
from datetime import datetime
import os
import ssl

# SSL 인증서 문제 해결
ssl._create_default_https_context = ssl._create_unverified_context

# 전역 변수
current_model = None
current_model_size = "small"

def process_audio(audio_file, model_size, progress=gr.Progress()):
    """오디오 파일을 텍스트로 변환"""
    global current_model, current_model_size

    if audio_file is None:
        return "❌ 파일을 업로드해주세요."

    try:
        progress(0.1, desc="모델 준비 중...")

        # 모델 로드
        if current_model is None or current_model_size != model_size:
            if current_model is None:
                gr.Info("⏳ 처음 실행 시 모델 다운로드로 시간이 소요됩니다. (약 1-5분)\n다음 변환부터는 빠르게 실행됩니다!")
            elif current_model_size != model_size:
                gr.Info(f"⏳ {model_size} 모델을 다운로드 중입니다. 잠시만 기다려주세요.")

            progress(0.2, desc=f"{model_size} 모델 로드 중...")
            current_model = whisper.load_model(model_size)
            current_model_size = model_size

        # 음성 파일 변환
        progress(0.5, desc="음성 파일 변환 중...")
        result = current_model.transcribe(audio_file)
        text = result["text"]

        progress(1.0, desc="변환 완료!")
        gr.Info("✅ 변환이 완료되었습니다!")
        return text

    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"

def save_text_to_file(text, filename):
    """텍스트를 파일로 저장"""
    if not text or text.startswith("❌"):
        gr.Warning("❌ 저장할 텍스트가 없습니다.")
        return "❌ 저장할 텍스트가 없습니다."

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    if not filename or filename.strip() == "":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcription_{timestamp}"

    if not filename.endswith(".txt"):
        filename += ".txt"

    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        gr.Info(f"✅ 파일이 저장되었습니다: {filepath}")
        return f"✅ 저장 완료: {filepath}"
    except Exception as e:
        gr.Warning(f"❌ 저장 실패: {str(e)}")
        return f"❌ 저장 실패: {str(e)}"

def clear_all():
    """모든 입력과 출력 초기화"""
    return None, "", "", ""

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft(), title="MinutesAI") as demo:
    gr.Markdown(
        """
        # 🎙️ MinutesAI - 음성을 텍스트로 변환

        음성 파일이나 영상 파일을 업로드하면 AI가 자동으로 텍스트로 변환해드립니다.

        **지원 형식:** WAV, MP3, M4A, FLAC, OGG, OPUS, MP4, MKV, MOV, AVI, WEBM
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ 설정")

            model_selector = gr.Dropdown(
                choices=["tiny", "base", "small"],  # HF Spaces 무료 티어는 small까지만
                value="small",
                label="Whisper 모델 선택",
                info="small 권장 (무료 티어 제한)"
            )

            gr.Markdown("### 📁 파일 업로드")
            audio_input = gr.Audio(type="filepath", label="음성/영상 파일 선택")

            convert_btn = gr.Button("🔄 텍스트로 변환하기", variant="primary", size="lg")
            clear_btn = gr.Button("🗑️ 전체 초기화", variant="secondary")

        with gr.Column(scale=2):
            gr.Markdown("### 📝 변환된 텍스트")
            text_output = gr.Textbox(
                label="텍스트 (편집 가능)",
                lines=20,
                placeholder="변환된 텍스트가 여기에 표시됩니다.",
                show_copy_button=True
            )

            gr.Markdown("### 💾 저장")
            with gr.Row():
                filename_input = gr.Textbox(
                    label="파일명",
                    placeholder="예: meeting_notes",
                    scale=3
                )
                save_btn = gr.Button("💾 저장", variant="secondary", scale=1, size="lg")

            save_status = gr.Textbox(label="저장 상태", interactive=False, show_label=False)

    # 이벤트 연결
    convert_btn.click(fn=process_audio, inputs=[audio_input, model_selector], outputs=text_output)
    save_btn.click(fn=save_text_to_file, inputs=[text_output, filename_input], outputs=save_status)
    clear_btn.click(fn=clear_all, inputs=[], outputs=[audio_input, text_output, filename_input, save_status])

    gr.Markdown("---\nMade with ❤️ using [OpenAI Whisper](https://github.com/openai/whisper)")

if __name__ == "__main__":
    demo.launch()
