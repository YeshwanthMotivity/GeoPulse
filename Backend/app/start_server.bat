@echo off
echo ==================================================
echo   Correcting path and starting server...
echo ==================================================
cd ..
uvicorn app.main:app --reload
pause
