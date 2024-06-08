import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser
import os
import signal
import time
import threading
import psutil

app_process = None

def download_python():
    webbrowser.open("https://www.python.org/downloads/")

def install_requirements():
    def run_pip_install():
        process = subprocess.Popen(
            ["pip", "install", "-r", "requirements.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            text_box.insert(tk.END, line)
            text_box.see(tk.END)
        process.wait()
        if process.returncode == 0:
            messagebox.showinfo("완료", "라이브러리 설치가 완료되었습니다.")
        else:
            messagebox.showerror("오류", "라이브러리 설치 중 오류가 발생했습니다.")
    
    threading.Thread(target=run_pip_install).start()

def show_app_output():
    global app_process
    for line in app_process.stdout:
        text_box.insert(tk.END, line)
        text_box.see(tk.END)

def run_app():
    global app_process
    if app_process is None:
        app_process = subprocess.Popen(["python", "app.py"], shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        threading.Thread(target=show_app_output).start()

        time.sleep(1)  # 앱이 시작할 시간을 줍니다.
        webbrowser.open("http://127.0.0.1:5000")

def close_app():
    global app_process
    if app_process is not None:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                for cmd in proc.cmdline():
                    if 'app.py' in cmd:
                        proc.terminate()
        app_process = None

app = tk.Tk()
app.title("Flask 프로젝트 관리자")
app.geometry("500x400")

button_frame = tk.Frame(app)
button_frame.pack(pady=20)

text_box = tk.Text(app, height=10, width=60)
text_box.pack(pady=10)

btn_download_python = tk.Button(button_frame, text="Download Python", command=download_python, width=20, height=2)
btn_download_python.grid(row=0, column=0, padx=5, pady=5)

btn_install_requirements = tk.Button(button_frame, text="Install Requirements", command=install_requirements, width=20, height=2)
btn_install_requirements.grid(row=0, column=1, padx=5, pady=5)

btn_run_app = tk.Button(button_frame, text="Run App", command=run_app, width=20, height=2)
btn_run_app.grid(row=1, column=0, padx=5, pady=5)

btn_close_app = tk.Button(button_frame, text="Close App", command=close_app, width=20, height=2)
btn_close_app.grid(row=1, column=1, padx=5, pady=5)

app.mainloop()
