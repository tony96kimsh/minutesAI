# MinutesAI 데스크톱 앱 빌드 가이드

## PyInstaller로 실행 파일 만들기

### 1. 준비

```bash
# PyInstaller 설치
pip install pyinstaller

# 프로젝트 디렉토리로 이동
cd /Users/gimseonghun/Project/minutesAI
```

### 2. 빌드 스크립트 작성

```bash
# build.sh
#!/bin/bash

pyinstaller \
    --name MinutesAI \
    --onefile \
    --windowed \
    --add-data "src:src" \
    --hidden-import=torch \
    --hidden-import=whisper \
    --hidden-import=gradio \
    --collect-all whisper \
    --collect-all gradio \
    src/gradio_app.py
```

### 3. 빌드 실행

```bash
chmod +x build.sh
./build.sh
```

### 4. 생성된 파일

```
dist/
└── MinutesAI          # macOS/Linux 실행 파일
    또는
    MinutesAI.exe      # Windows 실행 파일
```

### 5. 테스트

```bash
# macOS/Linux
./dist/MinutesAI

# Windows
dist\MinutesAI.exe
```

실행하면 브라우저가 자동으로 열리고 http://localhost:7860 접속

---

## GitHub Releases로 배포

### 1. GitHub 저장소에 푸시

```bash
git add .
git commit -m "Add desktop app build"
git push origin main
```

### 2. Release 생성

1. GitHub 저장소 → "Releases" → "Create a new release"
2. Tag 생성: `v1.0.0`
3. Release title: `MinutesAI v1.0.0`
4. 파일 업로드:
   - `MinutesAI.exe` (Windows용)
   - `MinutesAI` (macOS용)
   - `MinutesAI-linux` (Linux용)

### 3. 사용자 다운로드

사용자는 다음 링크에서 다운로드:
```
https://github.com/YOUR_USERNAME/minutesAI/releases
```

---

## 더 나은 방법: GitHub Actions 자동 빌드

`.github/workflows/build.yml` 파일 생성:

```yaml
name: Build Desktop App

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build with PyInstaller
        run: |
          pyinstaller --name MinutesAI --onefile src/gradio_app.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: MinutesAI-${{ matrix.os }}
          path: dist/*
```

이렇게 하면 태그를 푸시할 때마다 자동으로 빌드됩니다!

---

## 대안: Nuitka (더 빠른 실행 파일)

PyInstaller 대신 Nuitka 사용:

```bash
pip install nuitka

python -m nuitka \
    --standalone \
    --onefile \
    --enable-plugin=torch \
    --enable-plugin=gradio \
    src/gradio_app.py
```

장점:
- 더 빠른 실행 속도
- 더 작은 파일 크기

단점:
- 빌드 시간 더 김
- 설정 복잡

---

## 주의사항

### 파일 크기
- 최소 500MB~1GB (Whisper 모델 포함)
- 모델을 제외하고 배포하려면 첫 실행 시 다운로드

### 보안
- 코드가 디컴파일될 수 있음
- 중요한 API 키는 포함하지 말 것

### 라이선스
- OpenAI Whisper는 MIT 라이선스
- 상업적 사용 가능
- 라이선스 명시 필요

---

## 사용자 문서 작성

README.md에 사용 방법 추가:

```markdown
## 다운로드 및 설치

### Windows
1. [Releases](https://github.com/YOUR_USERNAME/minutesAI/releases) 페이지 접속
2. `MinutesAI.exe` 다운로드
3. 더블클릭으로 실행
4. 브라우저가 자동으로 열립니다

### macOS
1. [Releases](https://github.com/YOUR_USERNAME/minutesAI/releases) 페이지 접속
2. `MinutesAI` 다운로드
3. 터미널에서 실행 권한 부여: `chmod +x MinutesAI`
4. 실행: `./MinutesAI`

### Linux
1. [Releases](https://github.com/YOUR_USERNAME/minutesAI/releases) 페이지 접속
2. `MinutesAI-linux` 다운로드
3. 터미널에서 실행 권한 부여: `chmod +x MinutesAI-linux`
4. 실행: `./MinutesAI-linux`
```
