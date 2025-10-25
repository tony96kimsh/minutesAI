# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MinutesAI is an AI-powered meeting transcription and summarization tool that converts audio/video files into text using Whisper STT (Speech-to-Text), then processes the transcriptions with LLM models for summarization.

**Technology Stack:**
- Python-based application
- OpenAI Whisper for speech-to-text conversion (local model execution)
- OpenAI API integration for LLM processing
- Gradio for web UI (implemented)
- Tkinter for file selection GUI (legacy CLI version)

## Development Workflow

The project follows this processing pipeline:
1. **File Input** → User selects audio/video file via GUI (FileHelper)
2. **STT Processing** → Whisper model transcribes audio to text (whisper_model)
3. **LLM Summarization** → Text processed by LLM for meeting minutes (llm_model - in progress)
4. **Output** → Formatted meeting minutes
5. **Future**: Interactive chatbot for Q&A about the transcript

## Code Architecture

### Core Modules

**Entry Points:**
- `src/main.py` - CLI version: Tkinter file dialog → STT → terminal output
- `src/gradio_app.py` - Web UI version: Browser-based interface with full features (recommended)

**File Management:**
- `src/FileHelper.py` - Tkinter-based file/folder selection utilities
  - `select_audio()`: Opens file dialog for Whisper-supported formats (wav, mp3, m4a, flac, ogg, opus, mp4, mkv, mov, avi, webm)
  - `select_file()`: General file selector
  - `select_folder()`: Folder selector

**STT Processing:**
- `src/whisper_model.py` - Whisper model management
  - `load_whisper_model(model_size)`: Loads Whisper model (default: "small")
  - `transcribe_audio(model, audio_path)`: Transcribes audio file to text
- `src/STT/whisperModel.py` - Empty placeholder (legacy)

**LLM Integration:**
- `src/llm_model.py` - Empty placeholder for LLM summarization (not yet implemented)
- `src/whisperAPI.py` - OpenAI API client setup (partially implemented, currently commented out)

### Directory Structure

```
src/
├── main.py              # Application entry point
├── FileHelper.py        # File selection utilities
├── whisper_model.py     # Whisper STT wrapper
├── whisperAPI.py        # OpenAI API client
├── llm_model.py         # LLM summarization (TODO)
├── STT/                 # STT module directory
├── FileIO/              # Empty directory
├── LLM/                 # Empty directory
└── test_audio/          # Sample audio files for testing
```

## Running the Application

### Web UI (Recommended)
```bash
cd src
python3 gradio_app.py
```

This will:
1. Start a web server on http://localhost:7860
2. Open browser automatically
3. Provide full-featured UI with:
   - File upload
   - Model selection (tiny/base/small/medium/large)
   - Progress bar
   - Text editing
   - File save functionality
   - Toast notifications

### CLI Version (Legacy)
```bash
cd src
python3 main.py
```

This will:
1. Open a Tkinter file dialog
2. Load the Whisper "small" model (downloads on first run)
3. Transcribe the audio to text
4. Print the transcribed text to terminal

## Environment Setup

**Required environment variables:**
Create a `.env` file in the project root:
```
API_KEY=your_openai_api_key
```

**Supported Whisper models:**
- `tiny` - Fastest, least accurate
- `base` - Fast, basic accuracy
- `small` - Default, balanced speed/accuracy
- `medium` - Slower, more accurate
- `large` - Slowest, most accurate

## Deployment

### Quick Public Share (Testing)
Set `share=True` in `gradio_app.py` to get a temporary public URL (expires in 72 hours)

### Hugging Face Spaces (Recommended for Production)
- Files prepared in `deployment/huggingface/`
- See `deployment/huggingface/README.md` for deployment guide
- Free CPU tier available
- GPU upgrade available ($0.60/hour)

### Docker (Self-hosted)
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:7860
```

### Comprehensive Deployment Guide
See `docs/deployment_guide.md` for detailed instructions on all deployment options

## Important Notes

- The project is in active development; LLM summarization (llm_model.py) is not yet implemented
- whisperAPI.py contains OpenAI client setup but is currently commented out
- Test audio files should be placed in `src/test_audio/`
- Whisper model files are downloaded to cache on first use (can be large, especially for 'large' model)
- SSL certificate verification is disabled in whisper_model.py for macOS compatibility
- Gradio web UI is fully functional and production-ready
