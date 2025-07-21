@echo off
cd /d C:\GC_Intellilab_Dashboard\LocalAIBridge
call venv\Scripts\activate.bat
streamlit run app/pages/instrument_dashboard.py
pause
