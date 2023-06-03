@echo off

cd /D "%~dp0"

set PATH=%PATH%;%SystemRoot%\system32

call wsl -e bash -lic "sed -i 's/\x0D$//' ./wsl.sh; source ./wsl.sh update"

:end
pause
