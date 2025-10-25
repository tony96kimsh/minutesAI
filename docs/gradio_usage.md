# Gradio UI 사용 가이드

## 목차
1. [Gradio 설치](#1-gradio-설치)
2. [기본 구조 이해](#2-기본-구조-이해)
3. [단계별 구현](#3-단계별-구현)
4. [실행 방법](#4-실행-방법)
5. [주요 컴포넌트](#5-주요-컴포넌트)

---

## 1. Gradio 설치

```bash
pip install gradio
```

---

## 2. 기본 구조 이해

Gradio UI는 다음과 같은 흐름으로 작동합니다:

```
Input 컴포넌트 (파일 업로드)
    ↓
처리 함수 (STT 변환)
    ↓
Output 컴포넌트 (텍스트 표시)
```

---

## 3. 단계별 구현

### Step 1: 간단한 Gradio 앱 만들기

가장 기본적인 형태의 Gradio 앱입니다.

```python
import gradio as gr

def process_audio(audio_file):
    """오디오 파일을 받아서 텍스트로 변환"""
    if audio_file is None:
        return "파일을 업로드해주세요."

    # 여기에 Whisper 변환 로직 추가
    return "변환된 텍스트가 여기 표시됩니다"

# UI 구성
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ 음성을 텍스트로 변환")

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="음성 파일 업로드")

    with gr.Row():
        convert_btn = gr.Button("변환하기")

    with gr.Row():
        text_output = gr.Textbox(label="변환된 텍스트", lines=10)

    # 버튼 클릭 시 실행
    convert_btn.click(fn=process_audio, inputs=audio_input, outputs=text_output)

demo.launch()
```

---

### Step 2: 기존 Whisper 모델과 통합

기존 `whisper_model.py` 모듈을 Gradio와 연동합니다.

```python
import gradio as gr
import whisper_model  # 기존 모듈 import

# Whisper 모델 미리 로드 (앱 시작할 때 한 번만)
model = whisper_model.load_whisper_model("small")

def process_audio(audio_file):
    """오디오 파일을 텍스트로 변환"""
    if audio_file is None:
        return "파일을 업로드해주세요."

    try:
        # 기존 whisper_model 사용
        text = whisper_model.transcribe_audio(model, audio_file)
        return text
    except Exception as e:
        return f"오류 발생: {str(e)}"

# UI는 동일
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ 음성을 텍스트로 변환")

    audio_input = gr.Audio(type="filepath", label="음성 파일 업로드")
    convert_btn = gr.Button("변환하기")
    text_output = gr.Textbox(label="변환된 텍스트", lines=10)

    convert_btn.click(fn=process_audio, inputs=audio_input, outputs=text_output)

demo.launch()
```

**주요 변경사항:**
- `whisper_model` 모듈 import
- 앱 시작 시 모델 로드 (한 번만 실행)
- `process_audio()` 함수에서 실제 STT 변환 수행
- 에러 핸들링 추가

---

### Step 3: 텍스트 편집 및 저장 기능 추가

변환된 텍스트를 편집하고 파일로 저장하는 기능을 추가합니다.

```python
import gradio as gr
import whisper_model
from datetime import datetime
import os

model = whisper_model.load_whisper_model("small")

def process_audio(audio_file):
    """오디오 파일을 텍스트로 변환"""
    if audio_file is None:
        return "파일을 업로드해주세요."

    try:
        text = whisper_model.transcribe_audio(model, audio_file)
        return text
    except Exception as e:
        return f"오류 발생: {str(e)}"

def save_text(text):
    """텍스트를 파일로 저장"""
    if not text or text == "파일을 업로드해주세요.":
        return "저장할 텍스트가 없습니다."

    # 저장 디렉토리 생성
    os.makedirs("output", exist_ok=True)

    # 파일명에 타임스탬프 추가
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/transcription_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        return f"✅ 저장 완료: {filename}"
    except Exception as e:
        return f"❌ 저장 실패: {str(e)}"

# UI 구성
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ 음성을 텍스트로 변환")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(type="filepath", label="음성 파일 업로드")
            convert_btn = gr.Button("🔄 변환하기", variant="primary")

    with gr.Row():
        text_output = gr.Textbox(
            label="변환된 텍스트 (편집 가능)",
            lines=15,
            placeholder="변환된 텍스트가 여기 표시됩니다. 편집할 수 있습니다."
        )

    with gr.Row():
        save_btn = gr.Button("💾 텍스트 저장", variant="secondary")
        save_status = gr.Textbox(label="저장 상태", interactive=False)

    # 이벤트 연결
    convert_btn.click(fn=process_audio, inputs=audio_input, outputs=text_output)
    save_btn.click(fn=save_text, inputs=text_output, outputs=save_status)

demo.launch()
```

**추가된 기능:**
- `save_text()`: 텍스트를 파일로 저장하는 함수
- 자동 타임스탬프 파일명 생성
- `output/` 디렉토리 자동 생성
- 저장 상태 표시

---

### Step 4: 고급 기능 - 파일명 지정 & 모델 선택

사용자가 모델을 선택하고 파일명을 지정할 수 있는 완전한 기능의 UI입니다.

```python
import gradio as gr
import whisper_model
from datetime import datetime
import os

# 전역 모델 변수
current_model = None
current_model_size = "small"

def load_model(model_size):
    """선택한 모델 로드"""
    global current_model, current_model_size
    current_model_size = model_size
    current_model = whisper_model.load_whisper_model(model_size)
    return f"✅ {model_size} 모델 로드 완료"

def process_audio(audio_file, model_size):
    """오디오 파일을 텍스트로 변환"""
    global current_model, current_model_size

    if audio_file is None:
        return "파일을 업로드해주세요."

    try:
        # 모델이 변경되었으면 다시 로드
        if current_model is None or current_model_size != model_size:
            current_model = whisper_model.load_whisper_model(model_size)
            current_model_size = model_size

        text = whisper_model.transcribe_audio(current_model, audio_file)
        return text
    except Exception as e:
        return f"오류 발생: {str(e)}"

def save_text_with_name(text, filename):
    """사용자가 지정한 파일명으로 저장"""
    if not text or text.startswith("파일을") or text.startswith("오류"):
        return "저장할 텍스트가 없습니다."

    os.makedirs("output", exist_ok=True)

    # 파일명이 비어있으면 타임스탬프 사용
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcription_{timestamp}"

    # .txt 확장자 추가
    if not filename.endswith(".txt"):
        filename += ".txt"

    filepath = f"output/{filename}"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        return f"✅ 저장 완료: {filepath}"
    except Exception as e:
        return f"❌ 저장 실패: {str(e)}"

# UI 구성
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎙️ MinutesAI - 음성을 텍스트로 변환")
    gr.Markdown("음성/영상 파일을 업로드하면 텍스트로 변환해드립니다.")

    with gr.Row():
        with gr.Column(scale=1):
            # 모델 선택
            model_selector = gr.Dropdown(
                choices=["tiny", "base", "small", "medium", "large"],
                value="small",
                label="Whisper 모델 선택",
                info="small 권장 (속도와 정확도 균형)"
            )

            # 오디오 파일 업로드
            audio_input = gr.Audio(
                type="filepath",
                label="음성/영상 파일 업로드"
            )

            convert_btn = gr.Button("🔄 변환하기", variant="primary", size="lg")

        with gr.Column(scale=2):
            # 변환된 텍스트
            text_output = gr.Textbox(
                label="변환된 텍스트 (편집 가능)",
                lines=20,
                placeholder="변환된 텍스트가 여기 표시됩니다. 자유롭게 편집할 수 있습니다."
            )

    with gr.Row():
        filename_input = gr.Textbox(
            label="저장할 파일명",
            placeholder="예: meeting_notes (비워두면 자동 생성)",
            scale=3
        )
        save_btn = gr.Button("💾 저장", variant="secondary", scale=1)

    save_status = gr.Textbox(label="저장 상태", interactive=False)

    # 이벤트 연결
    convert_btn.click(
        fn=process_audio,
        inputs=[audio_input, model_selector],
        outputs=text_output
    )

    save_btn.click(
        fn=save_text_with_name,
        inputs=[text_output, filename_input],
        outputs=save_status
    )

demo.launch(share=False)  # share=True로 설정하면 공개 링크 생성
```

**추가된 고급 기능:**
- Whisper 모델 선택 (tiny, base, small, medium, large)
- 사용자 지정 파일명으로 저장
- 테마 적용 (`gr.themes.Soft()`)
- 레이아웃 비율 조정 (`scale` 파라미터)
- 더 나은 UI/UX (아이콘, 설명 텍스트)

---

## 4. 실행 방법

### 파일 생성
새 파일을 만듭니다:
```bash
touch src/gradio_app.py
```

### 코드 작성
위의 Step 4 코드를 `src/gradio_app.py`에 복사합니다.

### 실행
```bash
cd src
python gradio_app.py
```

### 접속
브라우저가 자동으로 열리고 `http://localhost:7860`에서 UI를 확인할 수 있습니다.

### 종료
터미널에서 `Ctrl + C`를 누르면 서버가 종료됩니다.

---

## 5. 주요 컴포넌트

### Input 컴포넌트

| 컴포넌트 | 설명 | 예시 |
|---------|------|------|
| `gr.Audio()` | 오디오/비디오 파일 업로드 | `gr.Audio(type="filepath")` |
| `gr.Textbox()` | 텍스트 입력 | `gr.Textbox(label="입력")` |
| `gr.Dropdown()` | 드롭다운 선택 메뉴 | `gr.Dropdown(choices=["A", "B"])` |
| `gr.Slider()` | 슬라이더 | `gr.Slider(minimum=0, maximum=100)` |
| `gr.Checkbox()` | 체크박스 | `gr.Checkbox(label="동의")` |
| `gr.Radio()` | 라디오 버튼 | `gr.Radio(choices=["옵션1", "옵션2"])` |

### Output 컴포넌트

| 컴포넌트 | 설명 | 예시 |
|---------|------|------|
| `gr.Textbox()` | 텍스트 출력 | `gr.Textbox(interactive=False)` |
| `gr.Label()` | 레이블 출력 | `gr.Label()` |
| `gr.Image()` | 이미지 출력 | `gr.Image()` |
| `gr.Audio()` | 오디오 출력 | `gr.Audio()` |
| `gr.File()` | 파일 다운로드 | `gr.File()` |

### 레이아웃 컴포넌트

| 컴포넌트 | 설명 | 예시 |
|---------|------|------|
| `gr.Blocks()` | 자유로운 레이아웃 구성 | `with gr.Blocks():` |
| `gr.Row()` | 가로 배치 | `with gr.Row():` |
| `gr.Column()` | 세로 배치 | `with gr.Column():` |
| `gr.Tab()` | 탭 UI | `with gr.Tab("탭1"):` |
| `gr.Accordion()` | 접을 수 있는 섹션 | `with gr.Accordion("제목"):` |

### 기타 컴포넌트

| 컴포넌트 | 설명 | 예시 |
|---------|------|------|
| `gr.Button()` | 클릭 가능한 버튼 | `gr.Button("클릭", variant="primary")` |
| `gr.Markdown()` | 마크다운 렌더링 | `gr.Markdown("# 제목")` |
| `gr.HTML()` | HTML 렌더링 | `gr.HTML("<h1>제목</h1>")` |

---

## 6. 이벤트 연결

Gradio에서 버튼 클릭이나 입력 변경 시 함수를 실행하는 방법:

```python
# 버튼 클릭
button.click(fn=함수명, inputs=입력컴포넌트, outputs=출력컴포넌트)

# 입력 변경 시 자동 실행
textbox.change(fn=함수명, inputs=입력컴포넌트, outputs=출력컴포넌트)

# 파일 업로드 시 자동 실행
audio.upload(fn=함수명, inputs=입력컴포넌트, outputs=출력컴포넌트)

# 여러 입력 사용
button.click(
    fn=함수명,
    inputs=[input1, input2, input3],
    outputs=[output1, output2]
)
```

---

## 7. 실용 예제 - 프로그레스 바 추가

```python
import gradio as gr
import whisper_model
import time

model = whisper_model.load_whisper_model("small")

def process_with_progress(audio_file, progress=gr.Progress()):
    """진행 상황을 표시하며 변환"""
    if audio_file is None:
        return "파일을 업로드해주세요."

    progress(0, desc="변환 시작...")
    time.sleep(0.5)

    progress(0.3, desc="오디오 파일 분석 중...")
    time.sleep(0.5)

    progress(0.6, desc="텍스트 변환 중...")
    text = whisper_model.transcribe_audio(model, audio_file)

    progress(1.0, desc="완료!")
    return text

with gr.Blocks() as demo:
    gr.Markdown("# 프로그레스 바 예제")

    audio_input = gr.Audio(type="filepath")
    convert_btn = gr.Button("변환")
    text_output = gr.Textbox(lines=10)

    convert_btn.click(
        fn=process_with_progress,
        inputs=audio_input,
        outputs=text_output
    )

demo.launch()
```

---

## 8. 유용한 launch() 옵션

```python
demo.launch(
    share=False,           # True로 설정하면 공개 URL 생성
    server_name="0.0.0.0", # 외부 접속 허용
    server_port=7860,      # 포트 번호 지정
    debug=True,            # 디버그 모드
    show_error=True        # 에러 메시지 표시
)
```

---

## 9. 참고 자료

- [Gradio 공식 문서](https://www.gradio.app/docs)
- [Gradio 예제 모음](https://www.gradio.app/demos)
- [Gradio GitHub](https://github.com/gradio-app/gradio)
