#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

if [[ "$(pwd)" =~ " " ]]; then echo This script relies on Miniconda which can not be silently installed under a path with spaces. && exit; fi

OS_ARCH=$(uname -m)
case "${OS_ARCH}" in
    x86_64*)    OS_ARCH="x86_64";;
    arm64*)     OS_ARCH="aarch64";;
    *)          echo "Unknown system architecture: $OS_ARCH! This script runs only on x86_64 or arm64" && exit
esac

# config
INSTALL_DIR="$(pwd)/installer_files"
CONDA_ROOT_PREFIX="$(pwd)/installer_files/conda"
INSTALL_ENV_DIR="$(pwd)/installer_files/env"

# activate installer env
source "$CONDA_ROOT_PREFIX/etc/profile.d/conda.sh" # otherwise conda complains about 'shell not initialized' (needed when running in a script)
conda activate "$INSTALL_ENV_DIR"

# update installer env
python webui.py --update

echo

