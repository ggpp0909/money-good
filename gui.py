import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser
import os
import signal

class FlaskAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flask Project Automation")
        
        self.python_button = tk.Button(root, text="Download Python", command=self.download_python)
        self.python_button.pack(pady=10)

        self.library_button = tk.Button(root, text="Download Libraries", command=self.download_libraries)
        self.library_button.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Run App", command=self.run_app)
        self.start_button.pack(pady=10)
        
        self.close_button = tk.Button(root, text="Close App", command=self.close_app)
        self.close_button.pack(pady=10)
        
        self.app_process = None
    
    def download_python(self):
        webbrowser.open("https://www.python.org/downloads/")
    
    def download_libraries(self):
        try:
            subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
            messagebox.showinfo("Success", "All libraries installed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install libraries: {e}")
    
    def run_app(self):
        if self.app_process is None:
            self.app_process = subprocess.Popen(["python", "app.py"])
            webbrowser.open("http://localhost:5000")  # 기본 플라스크 URL
            messagebox.showinfo("Success", "Flask app is running.")
        else:
            messagebox.showwarning("Warning", "Flask app is already running.")
    
    def close_app(self):
        if self.app_process is not None:
            try:
                os.kill(self.app_process.pid, signal.SIGTERM)
                self.app_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.kill(self.app_process.pid, signal.SIGKILL)
            self.app_process = None
            messagebox.showinfo("Success", "Flask app has been closed.")
        else:
            messagebox.showwarning("Warning", "Flask app is not running.")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = FlaskAppGUI(root)
    root.mainloop()
