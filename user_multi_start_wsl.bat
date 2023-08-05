@echo off
setlocal enabledelayedexpansion

:: Instance Data: LISTEN_PORT, API_BLOCKING_PORT, API_STREAMING_PORT, STATIC_FLAGS
set "INSTANCE_DATA[0]=46527,42768,42769,--model TheBloke_vicuna-7B-v1.5-GPTQ --loader gptq-for-llama  --wbits 4 --groupsize 128 --monkey-patch --xformers --n-gpu-layers 200000"
set "INSTANCE_DATA[1]=36527,32768,32769,--model TheBloke_vicuna-7B-v1.3-GPTQ --loader gptq-for-llama  --wbits 4 --groupsize 128 --monkey-patch --xformers --n-gpu-layers 200000"
::set "INSTANCE_DATA[1]=1,2,3,4"



echo Debug: Array 0: !INSTANCE_DATA[0]!
echo Debug: Array 1: !INSTANCE_DATA[1]!
:: ... add more instances as needed ...

:: Detect WSL IP address
FOR /F %%a IN ('wsl -e bash -c "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -f1 -d '/'"') DO SET WslIP=%%a

echo Detected WSL IP: %WslIP%

:: Detect Windows IP address for the Ethernet interface
FOR /F %%a IN ('powershell -command "Get-NetIPConfiguration | Where-Object { $_.InterfaceAlias -eq 'Ethernet' } | ForEach-Object { $_.IPv4Address.IPAddress }"') DO SET WinIP=%%a

echo Detected Win IP: %WinIP%


:: Loop through instances and set ports
for /L %%j in (0,1,9) do (
    if defined INSTANCE_DATA[%%j] (
        set "currentInstance=!INSTANCE_DATA[%%j]!"
        echo Instance Data for %%j is: !currentInstance!
        
        :: Extract data for current instance
        for /f "tokens=1-4 delims=," %%a in ("!currentInstance!") do (
            set LISTEN_PORT=%%a
            set API_BLOCKING_PORT=%%b
            set API_STREAMING_PORT=%%c
            set STATIC_FLAGS=%%d
        )

        echo Starting instance with ports:
        echo LISTEN_PORT: !LISTEN_PORT!
        echo API_BLOCKING_PORT: !API_BLOCKING_PORT!
        echo API_STREAMING_PORT: !API_STREAMING_PORT!

        :: Use netsh to setup the port redirection
        netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=!LISTEN_PORT!
        netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=!API_BLOCKING_PORT!
        netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=!API_STREAMING_PORT!

        netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=!LISTEN_PORT! connectaddress=%WslIP% connectport=!LISTEN_PORT!

        if ERRORLEVEL 1 echo Failed to set up port forwarding for port !LISTEN_PORT!

        netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=!API_BLOCKING_PORT! connectaddress=%WslIP% connectport=!API_BLOCKING_PORT!
        netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=!API_STREAMING_PORT! connectaddress=%WslIP% connectport=!API_STREAMING_PORT!
    

    
    
        :: Set the environment variable for flags
        set OOBABOOGA_FLAGS=--listen --api --verbose !STATIC_FLAGS! --listen-host "0.0.0.0" --listen-port "!LISTEN_PORT!" --api-blocking-port "!API_BLOCKING_PORT!" --api-streaming-port   "!API_STREAMING_PORT!"
    
        set "WSLENV=OOBABOOGA_FLAGS/u"

        :: Export environment variables to WSL and call the original script
        wsl -e bash -c "export OOBABOOGA_FLAGS='"'!OOBABOOGA_FLAGS!'"'"
    

        echo About to launch with:
        echo OOBABOOGA_FLAGS: !OOBABOOGA_FLAGS!

        :: Start the main script in a new process
        start call start_wsl.bat
    
        set "OOBABOOGA_FLAGS="

    )
)

:: Pause at the end for user to see the results
pause
