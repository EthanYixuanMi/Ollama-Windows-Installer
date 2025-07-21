import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import tkinter.scrolledtext as st

env_var_name = "OLLAMA_MODELS"
model_library_url = "https://ollama.com/library"

LANGUAGES = {
    "zh": {
        "title": "Ollama 快速安装器",
        "welcome": "欢迎使用 Ollama 快速安装器，请选择语言：",
        "step": "当前步骤：第 {step} 步，共 3 步",
        "open_download": "打开 Ollama 官网下载安装包",
        "confirm_downloaded": "我已在官网下载完成",
        "select_path": "请选择模型存储路径：",
        "browse": "浏览...",
        "set_env": "设置 OLLAMA_MODELS 环境变量",
        "model_list": "可选模型列表（点击安装）：",
        "warning_no_path": "请先选择路径",
        "success_env": "环境变量已设置为：",
        "confirm_pull": "是否下载模型：",
        "cancel_download": "❌ 取消下载",
        "download_complete": "模型 {model} 已成功下载。",
        "back": "返回",
        "language_toggle": "切换语言"
    },
    "en": {
        "title": "Ollama Quick Installer",
        "welcome": "Welcome to the Ollama Quick Installer. Please select a language:",
        "step": "Current Step: {step} of 3",
        "open_download": "Open Ollama website to download",
        "confirm_downloaded": "I have completed the download",
        "select_path": "Please select model storage path:",
        "browse": "Browse...",
        "set_env": "Set OLLAMA_MODELS environment variable",
        "model_list": "Available models (click to install):",
        "warning_no_path": "Please select a path first",
        "success_env": "Environment variable set to:",
        "confirm_pull": "Do you want to download the model:",
        "cancel_download": "❌ Cancel Download",
        "download_complete": "Model {model} has been successfully downloaded.",
        "back": "Back",
        "language_toggle": "Toggle Language"
    }
}

class OllamaInstallerApp:
    def __init__(self, root):
        self.root = root
        self.language = "zh"
        self.texts = LANGUAGES[self.language]
        self.models = []
        self.current_step = 1

        self.root.geometry("600x500")
        self.root.title(self.texts["title"])

        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill="x")
        self.step_label = tk.Label(self.header_frame, text="", font=("Arial", 10), anchor="w")
        self.step_label.pack(side="left", padx=10, pady=5)
        self.lang_btn = tk.Button(self.header_frame, text=self.texts["language_toggle"],
                                  command=self.toggle_language)
        self.lang_btn.pack(side="right", padx=10)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill="both")
        self.frames = {}
        self.create_frames()
        self.show_frame("welcome")

    def update_header(self):
        self.step_label.config(text=self.texts["step"].format(step=self.current_step))
        self.lang_btn.config(text=self.texts["language_toggle"])
        self.root.title(self.texts["title"])

    def toggle_language(self):
        self.language = "en" if self.language == "zh" else "zh"
        self.texts = LANGUAGES[self.language]
        self.rebuild_ui()

    def rebuild_ui(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        self.create_frames()
        self.show_frame(self.current_frame_name)

    def create_frames(self):
        self.frames["welcome"] = self.create_welcome_frame()
        self.frames["download"] = self.create_download_frame()
        self.frames["models"] = self.create_model_frame()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        self.current_frame_name = name
        self.current_step = {"welcome": 1, "download": 2, "models": 3}.get(name, 1)
        self.update_header()

    def create_welcome_frame(self):
        frame = tk.Frame(self.content_frame)
        label = tk.Label(frame, text=self.texts["welcome"], font=("Arial", 14))
        label.pack(pady=40)

        btn_zh = tk.Button(frame, text="中文", width=15, command=lambda: self.set_language("zh"))
        btn_zh.pack(pady=10)
        btn_en = tk.Button(frame, text="English", width=15, command=lambda: self.set_language("en"))
        btn_en.pack(pady=10)

        return frame

    def create_download_frame(self):
        frame = tk.Frame(self.content_frame)

        download_btn = tk.Button(frame, text=self.texts["open_download"], font=("Arial", 12), height=2, width=40,
                                 command=lambda: webbrowser.open("https://ollama.com/download/windows"))
        download_btn.pack(pady=40)

        confirm_btn = tk.Button(frame, text=self.texts["confirm_downloaded"], width=30,
                                command=lambda: self.show_frame("models"))
        confirm_btn.pack(pady=10)

        back_btn = tk.Button(frame, text=self.texts["back"], command=lambda: self.show_frame("welcome"))
        back_btn.pack(pady=20)

        return frame

    def create_model_frame(self):
        frame = tk.Frame(self.content_frame)

        path_label = tk.Label(frame, text=self.texts["select_path"])
        path_label.pack()

        self.path_entry = tk.Entry(frame, width=50)
        self.path_entry.pack()

        browse_btn = tk.Button(frame, text=self.texts["browse"], command=self.select_folder)
        browse_btn.pack()

        env_btn = tk.Button(frame, text=self.texts["set_env"], command=self.set_env_var)
        env_btn.pack(pady=10)

        model_label = tk.Label(frame, text=self.texts["model_list"])
        model_label.pack(pady=5)

        self.model_listbox = tk.Listbox(frame, width=50, height=15)
        self.model_listbox.pack()
        self.model_listbox.bind('<<ListboxSelect>>', self.model_selected)

        back_btn = tk.Button(frame, text=self.texts["back"], command=lambda: self.show_frame("download"))
        back_btn.pack(pady=10)

        self.load_models()

        return frame

    def set_language(self, lang):
        self.language = lang
        self.texts = LANGUAGES[self.language]
        self.rebuild_ui()
        self.show_frame("download")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)

    def set_env_var(self):
        path = self.path_entry.get()
        if not path:
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        os.system(f'setx {env_var_name} "{path}" /M')
        messagebox.showinfo(self.texts["title"], f"{self.texts['success_env']} {path}")

    def load_models(self):
        self.models = self.fetch_online_models()
        self.model_listbox.delete(0, tk.END)
        for model in self.models:
            self.model_listbox.insert(tk.END, model)

    def fetch_online_models(self):
        try:
            response = requests.get(model_library_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            model_list = []
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("/library/"):
                    model = a["href"].split("/library/")[1]
                    if model and model not in model_list:
                        model_list.append(model)
            return model_list
        except Exception as e:
            print(f"⚠️ 模型列表获取失败，使用默认列表: {e}")
            return ["llama3", "phi3", "mistral", "deepseek-coder", "codellama"]

    def model_selected(self, event):
        if not self.path_entry.get():
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        selected = self.model_listbox.get(self.model_listbox.curselection())
        if messagebox.askyesno(self.texts["title"], f"{self.texts['confirm_pull']} {selected}?"):
            self.pull_model(selected)

    def pull_model(self, model_name):
        def run_pull():
            try:
                startupinfo = None
                if sys.platform == "win32":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                process = subprocess.Popen(
                    ["ollama", "pull", model_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",  # 👈 关键修改
                    errors="replace",  # 👈 防止乱码崩溃
                    startupinfo=startupinfo
                )
                self.show_download_window(process, model_name)
            except Exception as e:
                messagebox.showerror("错误", f"下载失败：{e}")

        threading.Thread(target=run_pull, daemon=True).start()

    def show_download_window(self, process, model_name):
        win = tk.Toplevel(self.root)
        win.title(f"正在下载：{model_name}")
        win.geometry("600x400")

        style = ttk.Style(win)
        style.theme_use('default')
        style.configure("green.Horizontal.TProgressbar", troughcolor='white', bordercolor='black',
                        background='green', lightcolor='green', darkcolor='green')

        progress = ttk.Progressbar(win, orient='horizontal', length=500, mode='determinate',
                                   style="green.Horizontal.TProgressbar", maximum=100)
        progress.pack(pady=5)

        log_area = st.ScrolledText(win, wrap=tk.WORD)
        log_area.pack(expand=True, fill=tk.BOTH)

        cancel_btn = tk.Button(win, text=self.texts["cancel_download"], fg="red",
                               command=lambda: cancel_download())
        cancel_btn.pack(pady=5)

        steps = ["pulling manifest", "pulling layers", "extracting", "verifying", "success"]
        completed_steps = set()
        cancelled = False

        def cancel_download():
            nonlocal cancelled
            cancelled = True
            try:
                process.terminate()
            except Exception:
                pass
            progress.stop()
            log_area.insert(tk.END, "\n❌ 下载已取消。\n")
            log_area.see(tk.END)
            cancel_btn.config(state=tk.DISABLED)
            win.title("下载已取消")

        def read_output():
            nonlocal cancelled
            for line in process.stdout:
                if cancelled:
                    break
                log_area.insert(tk.END, line)
                log_area.see(tk.END)

                for i, step in enumerate(steps):
                    if step in line and step not in completed_steps:
                        completed_steps.add(step)
                        percent = int((len(completed_steps)) / len(steps) * 100)
                        progress["value"] = percent
                        break

            process.wait()
            if not cancelled:
                if process.returncode == 0:
                    progress["value"] = 100
                    log_area.insert(tk.END, f"\n✅ 模型 {model_name} 下载完成。\n")
                    log_area.see(tk.END)
                    messagebox.showinfo("下载完成", self.texts["download_complete"].format(model=model_name))
                    win.title("下载完成")
                else:
                    log_area.insert(tk.END, f"\n❌ 下载失败，错误码：{process.returncode}\n")
                    log_area.see(tk.END)
                    win.title("下载失败")
            cancel_btn.config(state=tk.DISABLED)

        threading.Thread(target=read_output, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaInstallerApp(root)
    root.mainloop()
