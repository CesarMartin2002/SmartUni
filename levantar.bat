@echo off
cd CODIGO
start "Levantamiento" /B cmd /c call env\Scripts\python.exe -m uvicorn --app-dir=BACK/ main:app --host 0.0.0.0 --reload
cd ..
