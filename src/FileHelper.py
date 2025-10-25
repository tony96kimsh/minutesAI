# FileHelper.py
import tkinter as tk
from tkinter import filedialog

def select_file():
    """
    파일 탐색기를 열고 사용자가 선택한 파일 경로를 반환한다.
    선택이 취소되면 None을 반환한다.
    """
    root = tk.Tk()
    root.withdraw()  # Tkinter 기본 창 숨기기

    file_path = filedialog.askopenfilename(
        title="파일 선택",
        filetypes=[("모든 파일", "*.*")]  # 필요시 확장자 필터 추가 가능
    )

    if file_path:
        return file_path
    else:
        return None

def select_folder():
    """
    폴더 탐색기를 열고 사용자가 선택한 폴더 경로를 반환한다.
    선택이 취소되면 None을 반환한다.
    """
    root = tk.Tk()
    root.withdraw()  # Tkinter 기본 창 숨기기

    folder_path = filedialog.askdirectory(title="폴더 선택")

    if folder_path:
        return folder_path
    else:
        return None
    

def select_audio():
    """
    Whisper에서 지원하는 오디오/비디오 파일만 선택할 수 있는 파일 탐색기를 연다.
    선택이 취소되면 None을 반환한다.
    """
    root = tk.Tk()
    root.withdraw()  # Tkinter 기본 창 숨기기

    filetypes = [
        ("Whisper 지원 파일", "*.wav *.mp3 *.m4a *.flac *.ogg *.opus *.mp4 *.mkv *.mov *.avi *.webm"),
        ("오디오 파일", "*.wav *.mp3 *.m4a *.flac *.ogg *.opus"),
        ("비디오 파일", "*.mp4 *.mkv *.mov *.avi *.webm"),
        ("모든 파일", "*.*")  # 옵션으로 전체 열기 가능
    ]

    file_path = filedialog.askopenfilename(
        title="음성을 글로 변환할 파일 선택",
        filetypes=filetypes
    )

    return file_path if file_path else None