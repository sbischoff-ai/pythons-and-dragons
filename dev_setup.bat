@ECHO off
ECHO Only run this once!
ECHO Create venv, add path to PYTHONPATH and install dependencies?
SET /p continue=[y/n] 
IF %continue%==n EXIT
ECHO Input path to Python Distribution (directory containing python.exe)
SET /p path=(without slash at the end): 
ECHO ##################################
ECHO Creating Virtual Environment ...
ECHO ##################################
MKDIR %~dp0venv
%path%\python.exe -m venv %~dp0venv
ECHO ##################################
ECHO Activating Virtual Environment ...
ECHO ##################################
ECHO Appending Development Directory to PYTHONPATH ...
> %~dp0venv\Lib\site-packages\pnd.pth ECHO %~dp0
ECHO ##################################
ECHO Installing Dependencies ...
ECHO ##################################
%~dp0venv\Scripts\python.exe -m pip install --upgrade pip
%~dp0venv\Scripts\python.exe -m pip install -r %~dp0requirements.txt
ECHO ##################################
ECHO Dev Setup completed.
ECHO Use .\venv environment for testing.
ECHO To start, execute 'python -m pnd' in activated environment
ECHO ##################################
PAUSE