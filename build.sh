#!/bin/bash

# MinutesAI 빌드 스크립트

echo "🚀 MinutesAI 빌드 시작..."
echo ""

# 기존 빌드 제거
echo "📦 기존 빌드 정리 중..."
rm -rf build dist

# PyInstaller 빌드 실행
echo "🔨 PyInstaller 빌드 실행 중..."
echo "   (시간이 다소 걸릴 수 있습니다: 5-10분)"
echo ""

pyinstaller build.spec

# 빌드 결과 확인
if [ -d "dist/MinutesAI.app" ]; then
    echo ""
    echo "✅ 빌드 성공!"
    echo ""
    echo "📂 생성된 파일:"
    echo "   dist/MinutesAI.app"
    echo ""
    echo "🧪 테스트 실행:"
    echo "   open dist/MinutesAI.app"
    echo ""
    echo "   또는"
    echo "   ./dist/MinutesAI/MinutesAI"
    echo ""
else
    echo ""
    echo "❌ 빌드 실패!"
    echo "   로그를 확인하세요."
    exit 1
fi
