@ECHO off
ECHO Only run this once!
ECHO Create venv, add path to PYTHONPATH and install dependencies?
SET /p continue=[y/n] 
IF %continue%==n EXIT
SET /p path=Input path to Python Distribution (with backslashes): 
ECHO ##################################
ECHO Creating Virtual Environment ...
ECHO ##################################
MKDIR %~dp0venv
CALL %path%\Scripts\activate.bat
ECHO python activated, creating venv ...
python -m venv %~dp0venv
ECHO ##################################
ECHO Activating Virtual Environment ...
ECHO ##################################
CALL %~dp0venv\Scripts\activate.bat
ECHO Appending Development Directory to PYTHONPATH ...
> %~dp0venv\Lib\site-packages\pnd.pth ECHO %~dp0
ECHO ##################################
ECHO Installing Dependencies ...
ECHO ##################################
python -m pip install --upgrade pip
pip install pytest
pip install appdirs
ECHO ##################################
ECHO Dev Setup completed.
ECHO Use .\venv environment for testing
ECHO ##################################
PAUSE