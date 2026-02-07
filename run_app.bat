@echo off
cd /d C:\Data\PythonToBrowserApp
call .venv\Scripts\activate
python -m streamlit run app.py
pause
