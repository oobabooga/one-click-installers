@echo off

@echo Starting the web UI...

cd /D "%~dp0"

set MAMBA_ROOT_PREFIX=%cd%\installer_files\mamba
set INSTALL_ENV_DIR=%cd%\installer_files\env

if not exist "%MAMBA_ROOT_PREFIX%\condabin\micromamba.bat" (
  call "%MAMBA_ROOT_PREFIX%\micromamba.exe" shell hook >nul 2>&1
)
call "%MAMBA_ROOT_PREFIX%\condabin\micromamba.bat" activate "%INSTALL_ENV_DIR%" || ( echo MicroMamba hook not found. && goto end )

:choose_extensions
cd text-generation-webui\extensions
@echo Available extensions:
setlocal enabledelayedexpansion
set count=0
for /D %%d in (*) do (
  set /A count+=1
  set "extension[!count!]=%%d"
  echo !count!: %%d
)

set /p choices=Enter the numbers of the extensions to use (separate multiple numbers with a space):

set extensions=
for %%c in (%choices%) do (
  set "ext=!extension[%%c]!"
  if defined extensions (
    set "extensions=!extensions! !ext!"
  ) else (
    set "extensions=!ext!"
  )
)

cd ..

set command=python server.py --auto-devices --model vicuna-13b-GPTQ-4bit-128g --wbits 4 --groupsize 128 --listen --listen-port 7861 --extensions %extensions%

@echo The following command will be run:
@echo %command%

set /p confirm=Do you want to run this command? (y/n):

if /i "%confirm%"=="y" (
  %command%
) else (
  cd ..
  goto choose_extensions
)

:end
pause
