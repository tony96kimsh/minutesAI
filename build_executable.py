"""
PyInstaller를 사용해 실행 파일(.exe, .app) 생성
"""

# 1. PyInstaller 설치
# pip install pyinstaller

# 2. 빌드 명령어
# pyinstaller --name MinutesAI \
#             --onefile \
#             --windowed \
#             --add-data "src:src" \
#             --icon icon.ico \
#             src/gradio_app.py

# 생성된 파일: dist/MinutesAI.exe (Windows) 또는 dist/MinutesAI.app (macOS)

# GitHub Releases에 업로드하여 배포
