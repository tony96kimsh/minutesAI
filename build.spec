# -*- mode: python ; coding: utf-8 -*-
# MinutesAI PyInstaller Build Specification

import os
from PyInstaller.utils.hooks import collect_all, collect_data_files

# 작업 디렉토리
block_cipher = None
project_dir = os.path.abspath('.')

# Gradio 데이터 수집
gradio_datas, gradio_binaries, gradio_hiddenimports = collect_all('gradio')
gradio_client_datas, gradio_client_binaries, gradio_client_hiddenimports = collect_all('gradio_client')

# safehttpx 데이터 수집 (Gradio 의존성)
safehttpx_datas, safehttpx_binaries, safehttpx_hiddenimports = collect_all('safehttpx')

# Whisper 데이터 수집
whisper_datas = collect_data_files('whisper')

a = Analysis(
    ['src/gradio_app.py'],
    pathex=[project_dir],
    binaries=gradio_binaries + gradio_client_binaries + safehttpx_binaries,
    datas=gradio_datas + gradio_client_datas + safehttpx_datas + whisper_datas,
    hiddenimports=[
        'gradio',
        'gradio_client',
        'safehttpx',
        'whisper',
        'torch',
        'torchaudio',
        'openai',
        'tiktoken',
        'numba',
        'ssl',
        'certifi',
    ] + gradio_hiddenimports + gradio_client_hiddenimports + safehttpx_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MinutesAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # True로 설정하여 터미널 창 표시 (진행 상황 확인용)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MinutesAI',
)

# macOS용 앱 번들
app = BUNDLE(
    coll,
    name='MinutesAI.app',
    icon=None,
    bundle_identifier='com.minutesai.app',
)
