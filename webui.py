import argparse
import glob
import os
import shutil
import site
import subprocess
import sys

def run_cmd(cmd, capture_output=False):
    return subprocess.run(cmd, shell=True, capture_output=capture_output)

def check_env():
    conda_not_exist = run_cmd("conda", capture_output=True).returncode
    if conda_not_exist:
        print("Conda is not installed. Exiting...")
        sys.exit()
    
    if os.environ["CONDA_DEFAULT_ENV"] == "base":
        print("Create an environment for this project and activate it. Exiting...")
        sys.exit()

def install_dependencies():
    site_packages_path = None
    for sitedir in site.getsitepackages():
        if "site-packages" in sitedir:
            site_packages_path = sitedir
            break

    if site_packages_path is None:
        print("Could not find the path to your Python packages. Exiting...")
        sys.exit()

    print("What is your GPU")
    print()
    print("A) NVIDIA")
    print("B) AMD")
    print("C) Apple M Series")
    print("D) None (I want to run in CPU mode)")
    print()
    gpuchoice = input("Input> ").lower()

    if gpuchoice == "a":
        run_cmd("conda install -y pytorch[version=2,build=py3.10_cuda11.7*] torchvision torchaudio pytorch-cuda=11.7 cuda-toolkit ninja git -c pytorch -c nvidia/label/cuda-11.7.0 -c nvidia")
    elif gpuchoice == "b":
        print("AMD GPUs are not supported. Exiting...")
        sys.exit()
    elif gpuchoice == "c" or gpuchoice == "d":
        run_cmd("conda install -y pytorch torchvision torchaudio cpuonly git -c pytorch")
    else:
        print("Invalid choice. Exiting...")
        sys.exit()

    run_cmd("git clone https://github.com/oobabooga/text-generation-webui.git")
    if sys.platform.startswith("win"):
        run_cmd("python -m pip install https://github.com/jllllll/bitsandbytes-windows-webui/raw/main/bitsandbytes-0.37.2-py3-none-any.whl")
    
    update_dependencies()

    if gpuchoice == "d" or gpuchoice == "c":
        return
    
    if sys.platform.startswith("linux"):
        shutil.copy(os.path.join(site_packages_path, "bitsandbytes", "libbitsandbytes_cuda117.so"), os.path.join(site_packages_path, "bitsandbytes", "libbitsandbytes_cpu.so"))

    if not os.path.exists("repositories/"):
        os.mkdir("repositories")
    
    os.chdir("repositories")
    if not os.path.exists("GPTQ-for-LLaMa/"):
        run_cmd("git clone https://github.com/oobabooga/GPTQ-for-LLaMa.git -b cuda")
        os.chdir("GPTQ-for-LLaMa")
        run_cmd("python -m pip install -r requirements.txt")
        run_cmd("python setup_cuda.py install")
        
        quant_cuda_path_regex = os.path.join(site_packages_path, "quant_cuda*/")
        if not glob.glob(quant_cuda_path_regex):
            print("CUDA kernel compilation failed.")
            if sys.platform.startswith("win"):
                print("Attempting installation with wheel.")
                result = run_cmd("python -m pip install https://github.com/jllllll/GPTQ-for-LLaMa-Wheels/raw/main/quant_cuda-0.0.0-cp310-cp310-win_amd64.whl")
                if result.returncode == 1:
                    print("Wheel installation failed.")

def update_dependencies():
    os.chdir("text-generation-webui")
    run_cmd("git pull")

    run_cmd("python -m pip install -r requirements.txt --upgrade")
    extensions = next(os.walk("extensions"))[1]
    for extension in extensions:
        extension_req_path = os.path.join("extensions", extension, "requirements.txt")
        run_cmd("python -m pip install -r " + extension_req_path + " --upgrade")

def download_model():
    os.chdir("text-generation-webui")
    run_cmd("python download-model.py")

def run_model():
    os.chdir("text-generation-webui")
    run_cmd("python server.py --auto-devices --cai-chat")

if __name__ == "__main__":
    script_dir = os.getcwd()
    check_env()
    
    if not os.path.exists("text-generation-webui/"):
        install_dependencies()
        os.chdir(script_dir)
        download_model()
        os.chdir(script_dir)

    run_model()
