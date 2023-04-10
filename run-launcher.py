import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psutil
import webbrowser

try:
    import psutil
except ImportError:
    messagebox.showinfo("Info", "The 'psutil' module is not installed. Installing now...")
    os.system("pip install psutil")
    import psutil

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # Store the process ID of the command window
        self.cmd_proc = None
        self.master = master
        self.master.title("Web UI")
        self.master.configure(bg="#35393e")
        self.pack()
        self.create_widgets()
        self.directory_button = ttk.Button(self, text="Open directory", style="Custom.TButton", command=self.open_directory)
        self.directory_button.pack(fill=tk.X, padx=10, pady=5)

    def open_directory(self):
        os.startfile(os.getcwd())

    def create_widgets(self):
        self.model_label = ttk.Label(self, text="Model:", style="Custom.TLabel")
        self.model_label.pack(fill=tk.X, padx=10, pady=5)

        model_names = [name for name in os.listdir("text-generation-webui/models") if os.path.isdir(os.path.join("text-generation-webui/models", name))]
        self.model_var = tk.StringVar(value=model_names[0] if model_names else "")
        self.model_listbox = tk.Listbox(self, selectmode="single", exportselection=0, highlightthickness=0, borderwidth=0, background="#302c34", foreground="white", highlightbackground="#35393e", selectbackground="#7289DA", font=("Helvetica", 16))
        self.model_listbox.pack(fill=tk.X, padx=10, pady=5)

        for model in model_names:
            self.model_listbox.insert(tk.END, model)
			
        # Get the number of items in the mode_listbox
        num_models = len(self.model_listbox.get(0, tk.END))
		
		# Set the height of the mode_listbox based on the number of items
        self.model_listbox.config(height=min(num_models, 10))
		
        self.mode_label = ttk.Label(self, text="UI Mode:", foreground="white", background="#35393e", font=("Helvetica", 16), style="Custom.TLabel")
        self.mode_label.pack(fill=tk.X, padx=10, pady=5)

        self.mode_listbox_var = tk.StringVar(value=self.get_modes()[0] if self.get_modes() else "chat")
        if not self.mode_listbox_var.get():
            self.mode_listbox_var.set("chat")

        self.mode_listbox = tk.Listbox(self, selectmode="single", exportselection=0, highlightthickness=0, borderwidth=0, background="#302c34", foreground="white", highlightbackground="#35393e", selectbackground="#7289DA", font=("Helvetica", 16))
        self.mode_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for mode in self.get_modes():
            self.mode_listbox.insert(tk.END, mode)

        # Get the number of items in the mode_listbox
        num_modes = len(self.mode_listbox.get(0, tk.END))
		
		# Set the height of the mode_listbox based on the number of items
        self.mode_listbox.config(height=min(num_modes, 10))


        self.extensions_label = ttk.Label(self, text="Extensions:", foreground="white", background="#35393e", font=("Helvetica", 16))
        self.extensions_label.pack()

        self.extensions_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, exportselection=0, highlightthickness=0, borderwidth=0, background="#302c34", foreground="white", highlightbackground="#35393e", selectbackground="#7289DA", font=("Helvetica", 16))
        extensions_dir = os.path.join(os.getcwd(), "text-generation-webui", "extensions")
        for ext_name in os.listdir(extensions_dir):
            if os.path.isdir(os.path.join(extensions_dir, ext_name)):
                self.extensions_listbox.insert(tk.END, ext_name)
        self.extensions_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
		
		# Get the number of items in the mode_listbox
        num_ext = len(self.extensions_listbox.get(0, tk.END))
		
		# Set the height of the mode_listbox based on the number of items
        self.extensions_listbox.config(height=min(num_ext, 10))

        self.port_label = ttk.Label(self, text="Port:", style="Custom.TLabel", font=("TkDefaultFont", 16))
        self.port_label.pack(fill=tk.X, padx=10, pady=5)

        self.port_var = tk.StringVar(value="7860")
        self.port_entry = ttk.Entry(self, textvariable=self.port_var, width=6, style="Custom.TEntry")
        self.port_entry.pack(fill=tk.X, padx=10, pady=5)

        self.run_button = ttk.Button(self, text="Run", command=self.run_command, style="Custom.TButton")
        self.run_button.pack(fill=tk.X, padx=10, pady=5)

        self.shutdown_button = ttk.Button(self, text="Shutdown", command=self.shutdown_command, style="Custom.TButton")
        self.shutdown_button.pack(fill=tk.X, padx=10, pady=5)

    def get_models(self):
        models_dir = os.path.join(os.getcwd(), "text-generation-webui", "models")
        return [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]
		
    def get_modes(self):
        return ["chat", "notebook"]

    def get_extensions_arg(self):
        extensions = self.extensions_listbox.curselection()
        if extensions:
            extension_list = [self.extensions_listbox.get(idx) for idx in extensions]
            return "--extensions " + " ".join(list(set(extension_list)))
        else:
            return ""


    def run_command(self):
        # Get the selected items in the extensions listbox
        extensions_arg = self.get_extensions_arg()
        if "elevenlabs_tts" in extensions_arg:
            extensions_arg += " --no-stream"
        else:
            extensions_arg = extensions_arg
		    # Check if a model option has been selected
        #messagebox.showinfo("Extensions", extensions_arg)
        if not self.model_listbox.curselection():
            messagebox.showerror("Error", "Please select a model.")
            return
        model = [self.model_listbox.get(i) for i in self.model_listbox.curselection()]
        model = str(model).replace("[", "").replace("]", "").replace("'", "")
        model_arg = f"--model {model}" if model else ""
        port_number = self.port_var.get()
        chat_mode = [self.mode_listbox.get(i) for i in self.mode_listbox.curselection()]
        chat_mode = "--" + str(chat_mode).replace("[", "").replace("]", "").replace("'", "")
        if not chat_mode or chat_mode == "--":
            chat_mode = "--notebook"
        ##messagebox.showinfo(title="Extensions", message=chat_mode)
        cwd = os.getcwd()
        mamba_root_prefix = os.path.join(cwd, "installer_files", "mamba")
        install_env_dir = os.path.join(cwd, "installer_files", "env")
        command = f"cd {cwd}\\text-generation-webui && call {mamba_root_prefix}\\condabin\\micromamba.bat activate {install_env_dir} && python server.py --auto-devices {chat_mode} --listen --listen-port {port_number} {model_arg} --wbits 4 --groupsize 128 {extensions_arg}"
        os.system(f"start cmd /k \"{command}\"")
        webbrowser.open(f"http://localhost:{port_number}")


    def shutdown_command(self):
        try:
            for proc in psutil.process_iter():
                if proc.name() == "python.exe" and "server.py" in " ".join(proc.cmdline()):
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        os.system("taskkill /f /im cmd.exe")

root = tk.Tk()
root.minsize(400, 1)
root.configure(bg="#35393e")
root.tk_setPalette(background="#35393e", foreground="white", activeBackground="#35393e", activeForeground="white")
style = ttk.Style(root)
style.theme_use('clam')
style.configure("Custom.TButton", font=("Helvetica", 16), foreground="white", background="#7289DA", bordercolor="#99AAB5", borderwidth=1, anchor=tk.CENTER)
style.configure("Custom.TMenubutton", font=("Helvetica", 16), foreground="white", background="#7289DA", bordercolor="#99AAB5", borderwidth=1, anchor=tk.CENTER)
style.configure("Custom.TMenubutton.Menubutton", font=("Helvetica", 16), background="#36393F", foreground="white", anchor=tk.CENTER)
style.configure("Custom.TLabel", font=("Helvetica", 16), foreground="white", background="#35393e", anchor=tk.CENTER)
style.configure("Custom.TFrame", font=("Helvetica", 16), background="#36393F")
style.configure("Custom.TEntry", font=("Helvetica", 16), background="#40444B", foreground="white", bordercolor="#7289DA", borderwidth=1)
style.configure("Custom.TCombobox", font=("Helvetica", 16), foreground="white", background="#36393F", selectbackground="#7289DA", fieldbackground="#40444B")
style.configure("Custom.TSeparator", font=("Helvetica", 16), background="#36393F")
style.map("Custom.TButton", background=[("active", "#4E5D6C")], bordercolor=[("active", "#99AAB5")])
style.map("Custom.TMenubutton", background=[("active", "#4E5D6C")], bordercolor=[("active", "#99AAB5")])
style.configure("Custom.TEntry", foreground="white", background="#40444B", bordercolor="#7289DA", font=("Helvetica", 16), borderwidth=1)
style.map("Custom.TEntry", fieldbackground=[("focus", "#2C2F33",), ("!focus", "#40444B")])
		


app = App(master=root)
app.mainloop()

       
