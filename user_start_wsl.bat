@echo off

:: Default values
set DEFAULT_LISTEN_PORT=46527
set DEFAULT_API_BLOCKING_PORT=42768
set DEFAULT_API_STREAMING_PORT=42769

:: Ask the user for input or use the default values
set /P LISTEN_PORT="Enter listen port (default %DEFAULT_LISTEN_PORT%): "
IF "%LISTEN_PORT%"=="" set LISTEN_PORT=%DEFAULT_LISTEN_PORT%

set /P API_BLOCKING_PORT="Enter API blocking port (default %DEFAULT_API_BLOCKING_PORT%): "
IF "%API_BLOCKING_PORT%"=="" set API_BLOCKING_PORT=%DEFAULT_API_BLOCKING_PORT%

set /P API_STREAMING_PORT="Enter API streaming port (default %DEFAULT_API_STREAMING_PORT%): "
IF "%API_STREAMING_PORT%"=="" set API_STREAMING_PORT=%DEFAULT_API_STREAMING_PORT%


:: Detect WSL IP address
FOR /F %%a IN ('wsl -e bash -c "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -f1 -d '/'"') DO SET WslIP=%%a

:: Detect Windows IP address for the Ethernet interface
FOR /F %%a IN ('powershell -command "Get-NetIPConfiguration | Where-Object { $_.InterfaceAlias -eq 'Ethernet' } | ForEach-Object { $_.IPv4Address.IPAddress }"') DO SET WinIP=%%a

echo LISTEN_PORT: %LISTEN_PORT%
echo API_BLOCKING_PORT: %API_BLOCKING_PORT%
echo API_STREAMING_PORT: %API_STREAMING_PORT%
echo WinIP: %WinIP%
echo WslIP: %WslIP%


:: Use netsh to setup the port redirection
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=%LISTEN_PORT% connectaddress=%WslIP% connectport=%LISTEN_PORT%
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=%API_BLOCKING_PORT% connectaddress=%WslIP% connectport=%API_BLOCKING_PORT%
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=%API_STREAMING_PORT% connectaddress=%WslIP% connectport=%API_STREAMING_PORT%

:: Set the environment variable for flags
set OOBABOOGA_FLAGS=--listen --api --verbose --model TheBloke_vicuna-7B-v1.5-GPTQ --loader gptq-for-llama  --wbits 4 --groupsize 128 --monkey-patch --xformers --n-gpu-layers 200000  --listen-host "0.0.0.0" --listen-port "%LISTEN_PORT%" --api-blocking-port "%API_BLOCKING_PORT%" --api-streaming-port "%API_STREAMING_PORT%"

:: Export environment variables to WSL and call the original script
wsl -e bash -c "export OOBABOOGA_FLAGS='%OOBABOOGA_FLAGS%'"

:: Call the main script
call start_wsl.bat
