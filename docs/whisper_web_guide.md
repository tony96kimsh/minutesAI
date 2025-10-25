# Whisper Web - 브라우저에서 STT 실행하기

## 개념

Whisper.cpp를 WebAssembly로 컴파일하여 GitHub Pages에 배포하면:
- 웹사이트 접속만으로 STT 가능
- 사용자 PC의 브라우저에서 실행
- 서버 불필요, 완전히 클라이언트 사이드

## 구현 방법

### 1. 기존 오픈소스 프로젝트 사용 (가장 쉬움)

**Whisper Web:**
- https://github.com/xenova/whisper-web
- Transformers.js 기반
- GitHub Pages 배포 가능

**데모:**
- https://huggingface.co/spaces/Xenova/whisper-web

### 2. 직접 구현

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>MinutesAI Web</title>
    <script type="module">
        import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.6.0';

        // Whisper 모델 로드
        let transcriber = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny');

        async function transcribe(audioFile) {
            const result = await transcriber(audioFile);
            document.getElementById('output').textContent = result.text;
        }

        // 파일 업로드 핸들러
        document.getElementById('audioInput').addEventListener('change', (e) => {
            const file = e.target.files[0];
            transcribe(file);
        });
    </script>
</head>
<body>
    <h1>🎙️ MinutesAI Web</h1>
    <input type="file" id="audioInput" accept="audio/*">
    <div id="output"></div>
</body>
</html>
```

### 장점
- ✅ 설치 불필요
- ✅ GitHub Pages 배포 가능
- ✅ 웹 접속만으로 사용
- ✅ 완전히 무료

### 단점
- ❌ 모델 크기 제한 (tiny, base만 현실적)
- ❌ 성능이 Python 버전보다 낮음
- ❌ 구현 복잡도 높음

## GitHub Pages 배포

```bash
# 1. 정적 파일 준비
mkdir web-build
cd web-build

# 2. HTML, CSS, JS 파일 작성

# 3. GitHub 저장소 생성
git init
git add .
git commit -m "Initial commit"

# 4. GitHub Pages 활성화
# Repository Settings → Pages → Source: main branch

# 5. 접속
# https://USERNAME.github.io/minutesai-web
```

## 참고 자료

- [Transformers.js](https://github.com/xenova/transformers.js)
- [Whisper Web 예제](https://github.com/xenova/whisper-web)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
