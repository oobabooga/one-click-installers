@echo off

cd /D "%~dp0"

set PATH=%PATH%;%SystemRoot%\system32

@rem This will run a series of bash commands in WSL to activate conda env and open CLI   2 cd commands are used to allow the second to fail and still provide a CLI when webui is not installed
call wsl -- cd $HOME; cd ./text-gen-install; export INSTALL_DIR="$(pwd)"; export CONDA_ROOT_PREFIX="$INSTALL_DIR/installer_files/conda"; export INSTALL_ENV_DIR="$INSTALL_DIR/installer_files/env"; exec bash -lic "source $CONDA_ROOT_PREFIX/etc/profile.d/conda.sh; conda activate $INSTALL_ENV_DIR; exec bash"

:end
pause
