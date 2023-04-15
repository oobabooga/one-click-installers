@echo off

@echo Starting the web UI...

cd /D "%~dp0"

set INSTALL_ENV_DIR=%cd%\installer_files\env
set MINICONDA_DIR=%cd%\installer_files\miniconda3

if not exist "%MINICONDA_DIR%\Scripts\activate.bat" ( echo Miniconda not found. && goto end )
call "%MINICONDA_DIR%\Scripts\activate.bat" activate "%INSTALL_ENV_DIR%"
cd text-generation-webui

@rem set default cuda toolkit to the one in the environment
set "CUDA_PATH=%INSTALL_ENV_DIR%"

call python server.py --auto-devices --chat

:end
pause
