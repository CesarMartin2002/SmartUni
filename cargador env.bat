@echo off

echo Creating virtual environment...
python -m venv env

echo Activating virtual environment...
env\Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt

echo All done!
