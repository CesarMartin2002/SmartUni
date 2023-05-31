@echo off
cd CODIGO
start "Levantamiento" /B cmd /c call uvicorn --app-dir=BACK/ main:app --host 0.0.0.0 --reload
cd ..