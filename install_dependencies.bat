@echo off

REM Install Python dependencies from manga-ocr requirements
pip install -r manga-ocr\manga_ocr_dev\requirements.txt

REM Install Python dependencies for your scripts
pip install pynput tkinter customtkinter PIL pystray screeninfo
