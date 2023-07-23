# One Click Installers
Simplified installers for [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui).

## Installation
### One-click installation

| Windows | Linux | macOS | WSL |
|--------|--------|--------|--------|
| [oobabooga-windows.zip](https://github.com/oobabooga/text-generation-webui/releases/download/installers/oobabooga_windows.zip) | [oobabooga-linux.zip](https://github.com/oobabooga/text-generation-webui/releases/download/installers/oobabooga_linux.zip) |[oobabooga-macos.zip](https://github.com/oobabooga/text-generation-webui/releases/download/installers/oobabooga_macos.zip) | [oobabooga-wsl.zip](https://github.com/oobabooga/text-generation-webui/releases/download/installers/oobabooga_wsl.zip) |

Just download the zip above, extract it, and double-click on "start". The web UI and all its dependencies will be installed in the same folder.

* The source codes are here: https://github.com/oobabooga/one-click-installers
* There is no need to run the installers as admin.
* AMD doesn't work on Windows.
* Huge thanks to [@jllllll](https://github.com/jllllll), [@ClayShoaf](https://github.com/ClayShoaf), and [@xNul](https://github.com/xNul) for their contributions to these installers.

### Command-line installation
On Linux, it can be installed with these commands:
```
git clone https://github.com/oobabooga/one-click-installers
cd one-click-installers/
chmod +x start_linux.sh
./start_linux.sh 
```
Optionally, you can use command-line flags.<br> Example: If you want to create a public URL, you can set the flag in "OOBABOOGA_FLAGS" environment variable.
```
export OOBABOOGA_FLAGS="--share"
```
