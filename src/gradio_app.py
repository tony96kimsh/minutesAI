"""
MinutesAI Gradio UI
음성/영상 파일을 텍스트로 변환하는 웹 인터페이스
"""

import gradio as gr
import whisper_model
from datetime import datetime
import os

# 전역 변수
current_model = None
current_model_size = "small"

def process_audio(audio_file, model_size, progress=gr.Progress()):
    """
    오디오 파일을 텍스트로 변환

    Args:
        audio_file: 업로드된 오디오 파일 경로
        model_size: Whisper 모델 크기 (tiny, base, small, medium, large)
        progress: Gradio 프로그레스 바

    Returns:
        str: 변환된 텍스트 또는 에러 메시지
    """
    global current_model, current_model_size

    if audio_file is None:
        return "❌ 파일을 업로드해주세요."

    try:
        # 프로그레스 바 업데이트
        progress(0.1, desc="모델 준비 중...")

        # 모델이 변경되었거나 로드되지 않았으면 다시 로드
        if current_model is None or current_model_size != model_size:
            # 처음 로드하는 경우 토스트 메시지 표시
            if current_model is None:
                gr.Info("⏳ 처음 실행 시 모델 다운로드로 시간이 소요됩니다. (약 1-5분)\n다음 변환부터는 빠르게 실행됩니다!")
            elif current_model_size != model_size:
                gr.Info(f"⏳ {model_size} 모델을 다운로드 중입니다. 잠시만 기다려주세요.")

            progress(0.2, desc=f"{model_size} 모델 로드 중...")
            current_model = whisper_model.load_whisper_model(model_size)
            current_model_size = model_size

        # 음성 파일 변환
        progress(0.5, desc="음성 파일 변환 중... (파일이 길면 시간이 걸릴 수 있습니다)")
        text = whisper_model.transcribe_audio(current_model, audio_file)

        progress(1.0, desc="변환 완료!")
        gr.Info("✅ 변환이 완료되었습니다!")
        return text

    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"

def save_text_to_file(text, filename):
    """
    텍스트를 파일로 저장

    Args:
        text: 저장할 텍스트
        filename: 파일명 (확장자 제외 가능)

    Returns:
        str: 저장 상태 메시지
    """
    if not text or text.startswith("❌"):
        return "❌ 저장할 텍스트가 없습니다."

    # output 디렉토리 생성
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 파일명 처리
    if not filename or filename.strip() == "":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcription_{timestamp}"

    # .txt 확장자 추가
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

# Gradio UI 구성
with gr.Blocks(theme=gr.themes.Soft(), title="MinutesAI") as demo:
    # 헤더
    gr.Markdown(
        """
        # 🎙️ MinutesAI - 음성을 텍스트로 변환

        음성 파일이나 영상 파일을 업로드하면 AI가 자동으로 텍스트로 변환해드립니다.

        **지원 형식:** WAV, MP3, M4A, FLAC, OGG, OPUS, MP4, MKV, MOV, AVI, WEBM
        """
    )

    # 메인 레이아웃
    with gr.Row():
        # 왼쪽 컬럼 - 입력 영역
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ 설정")

            # 모델 선택
            model_selector = gr.Dropdown(
                choices=["tiny", "base", "small", "medium", "large"],
                value="small",
                label="Whisper 모델 선택",
                info="small 권장 (속도와 정확도의 균형)"
            )

            # 모델 크기 설명
            with gr.Accordion("📋 모델 크기 설명", open=False):
                gr.Markdown(
                    """
                    - **tiny**: 가장 빠름, 정확도 낮음 (~1GB 메모리)
                    - **base**: 빠름, 기본 정확도 (~1GB 메모리)
                    - **small**: 권장, 균형잡힌 성능 (~2GB 메모리)
                    - **medium**: 느림, 높은 정확도 (~5GB 메모리)
                    - **large**: 가장 느림, 최고 정확도 (~10GB 메모리)
                    """
                )

            gr.Markdown("### 📁 파일 업로드")

            # 오디오 파일 업로드
            audio_input = gr.Audio(
                type="filepath",
                label="음성/영상 파일 선택"
            )

            # 변환 버튼
            convert_btn = gr.Button(
                "🔄 텍스트로 변환하기",
                variant="primary",
                size="lg"
            )

            # 초기화 버튼
            clear_btn = gr.Button(
                "🗑️ 전체 초기화",
                variant="secondary"
            )

        # 오른쪽 컬럼 - 출력 영역
        with gr.Column(scale=2):
            gr.Markdown("### 📝 변환된 텍스트")

            # 변환된 텍스트 출력
            text_output = gr.Textbox(
                label="텍스트 (편집 가능)",
                lines=20,
                placeholder="변환된 텍스트가 여기에 표시됩니다.\n\n자유롭게 수정할 수 있습니다.",
                show_copy_button=True
            )

            # 파일 저장 영역
            gr.Markdown("### 💾 저장")

            with gr.Row():
                filename_input = gr.Textbox(
                    label="파일명",
                    placeholder="예: meeting_notes (비워두면 자동 생성)",
                    scale=3
                )
                save_btn = gr.Button(
                    "💾 저장",
                    variant="secondary",
                    scale=1,
                    size="lg"
                )

            save_status = gr.Textbox(
                label="저장 상태",
                interactive=False,
                show_label=False
            )

    # 사용 가이드
    with gr.Accordion("❓ 사용 방법", open=False):
        gr.Markdown(
            """
            ### 사용 단계

            1. **모델 선택**: 원하는 Whisper 모델을 선택합니다 (처음 사용 시 다운로드됨)
            2. **파일 업로드**: '음성/영상 파일 선택'을 클릭하여 파일을 업로드합니다
            3. **변환**: '텍스트로 변환하기' 버튼을 클릭합니다
            4. **편집**: 변환된 텍스트를 자유롭게 수정할 수 있습니다
            5. **저장**: 파일명을 입력하고 '저장' 버튼을 클릭합니다

            ### 팁

            - 짧은 파일은 **small** 모델로도 충분합니다
            - 긴 파일이나 음질이 나쁜 경우 **medium** 이상을 권장합니다
            - 처음 모델을 사용할 때는 다운로드 시간이 소요됩니다
            - 텍스트 박스에서 Ctrl+C로 복사할 수 있습니다
            """
        )

    # 이벤트 연결
    convert_btn.click(
        fn=process_audio,
        inputs=[audio_input, model_selector],
        outputs=text_output
    )

    save_btn.click(
        fn=save_text_to_file,
        inputs=[text_output, filename_input],
        outputs=save_status
    )

    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[audio_input, text_output, filename_input, save_status]
    )

    # 하단 정보
    gr.Markdown(
        """
        ---
        Made with ❤️ using [OpenAI Whisper](https://github.com/openai/whisper) and [Gradio](https://gradio.app)
        """
    )

# 앱 실행
if __name__ == "__main__":
    print("🚀 MinutesAI 시작 중...")
    print("📍 브라우저에서 http://localhost:7860 으로 접속하세요")

    demo.launch(
        server_name="0.0.0.0",  # 외부 접속 허용
        server_port=7860,        # 포트 번호
        share=False,             # 공개 링크 생성 안함 (True로 변경하면 인터넷에서 접속 가능)
        show_error=True          # 에러 메시지 표시
    )
