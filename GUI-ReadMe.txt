###Text Generation Web UI

This graphical user interface (GUI) provides an easy way to run the Text Generation Web UI server. The server can generate text using various deep learning models and can be used for a range of natural language processing tasks, such as text generation, language translation, and sentiment analysis. This readme file provides instructions for setting up and using the GUI.

###Config

You may need to modify the run run-launcher.py script to tweak command parameters not accessible from the interface. Go to line 138 to do so and look for the variable "command" be careful not to change anything but adding or removing prarams such as "--wbits 4 --groupsize 128" or you may break the GUI. 

###Usage

To run the GUI, execute the run.py script using Python. The GUI will appear, showing the available models and options. To run the server, follow these steps:

    Select a model from the list of available models.
    Choose a UI mode, such as chat or notebook.
    Select any desired extensions for the server.
    Enter a port number to use for the server (default is 7860).
    Click the "Run" button to start the server.

Once the server is running, a web browser window will automatically open, showing the server interface. You can use the server to generate text, translate languages, and perform other natural language processing tasks. The windo will open before the server has loaded so you will need to refresh after it finshes loading.

To shut down the server, click the "Shutdown" button in the GUI. This will terminate the server process and close any associated command prompt windows.

The Open directory button will open the working directory for oobabooga-windows.


###Troubleshooting

If you encounter any issues while using the GUI, try the following steps:

    Ensure that all prerequisites are installed correctly.
    Check that the selected model and options are correct.
    Verify that the server is running by checking the command prompt window.
    Check that the server is accessible by visiting http://localhost:7860 (or your choosen port) in a web browser.

If these steps do not resolve the issue, try searching online for solutions or ask for help from the developer or user community.