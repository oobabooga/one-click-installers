@echo off

SET TextOnly=False &REM True or False for Text only mode

cd /D "%~dp0"

set INSTALL_ENV_DIR=%cd%\installer_files\env
set MINICONDA_DIR=%cd%\installer_files\miniconda3

if not exist "%MINICONDA_DIR%\Scripts\activate.bat" ( echo Miniconda not found. && goto end )
call "%MINICONDA_DIR%\Scripts\activate.bat" activate "%INSTALL_ENV_DIR%"

cd text-generation-webui || goto end
goto %TextOnly%

:False
call python download-model.py
goto end

:True
call python download-model.py --text-only

:end
pause
