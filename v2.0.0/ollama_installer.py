import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import tkinter.scrolledtext as st
import re

"""Ollama Quick Installer — modernized UI (fixed navigation & improved sizing)
--------------------------------------------------------------------------
Summary of changes:
1. **Fix lingering on first page after language selection** → Language button calls `start_install()`, automatically goes to step 2.
2. **Increase overall scaling with default font** → `tk scaling 2`, default font 12 pt.
3. **Language switch button text fix** → zh: `"Switch to English"`; en: `"切换为中文"`.
"""

# ------------------------------------------------------------------
# ❶ Windows High-DPI awareness: prevents UI blurring / under-sizing
# ------------------------------------------------------------------
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per‑monitor v2
    except Exception:
        pass

# ------------------------------------------------------------------
# Constant Definition
# ------------------------------------------------------------------
env_var_name = "OLLAMA_MODELS"
model_library_url = "https://ollama.com/library"

LANGUAGES = {
    "zh": {
        # ---- Window & Navigation ----
        "title": "Ollama 快速安装器",
        "welcome": "欢迎使用 Ollama 快速安装器，请选择语言：",
        "step": "当前步骤：第 {step} 步，共 3 步",
        "back": "返回",
        "language_toggle": "Switch to English",

        # ---- Download page ----
        "open_download": "打开 Ollama 官网下载安装包",
        "confirm_downloaded": "我已下载完成",
        "local_install": "📦 安装本地版本",

        # ---- Model page ----
        "select_path": "请选择模型存储路径：",
        "browse": "浏览…",
        "set_env": "设置 OLLAMA_MODELS 环境变量",
        "model_list": "可选模型列表（点击安装）：",
        "warning_no_path": "请先选择路径",
        "success_env": "环境变量已设置为：",
        "confirm_pull": "是否下载模型：",

        # ---- Download dialog & progress ----
        "cancel_download": "❌ 取消下载",
        "downloading": "正在下载：{model}",
        "download_cancel_title": "下载已取消",
        "download_cancelled": "\n❌ 下载已取消。\n",
        "download_done_title": "下载完成",
        "download_complete": "模型 {model} 已成功下载。",
        "download_failed_title": "下载失败",
        "download_failed_code": "\n❌ 下载失败，错误码：{code}\n",

        # ---- Generic errors ----
        "error_title": "错误",
        "download_failed": "下载失败：{error}",
        "model_fetch_failed": "⚠️ 模型列表获取失败，使用默认列表: {error}",
        "local_exe_missing": "本地安装包 OllamaSetup.exe 未找到！",
        "local_exe_launch_error": "无法启动本地安装程序：{error}",
    },
    "en": {
        # ---- Window & Navigation ----
        "title": "Ollama Quick Installer",
        "welcome": "Welcome to the Ollama Quick Installer. Please select a language:",
        "step": "Current Step: {step} of 3",
        "back": "Back",
        "language_toggle": "切换为中文",

        # ---- Download page ----
        "open_download": "Open Ollama website to download",
        "confirm_downloaded": "I have completed the download",
        "local_install": "📦 Install Local Version",

        # ---- Model page ----
        "select_path": "Please select model storage path:",
        "browse": "Browse…",
        "set_env": "Set OLLAMA_MODELS environment variable",
        "model_list": "Available models (click to install):",
        "warning_no_path": "Please select a path first",
        "success_env": "Environment variable set to:",
        "confirm_pull": "Do you want to download the model:",

        # ---- Download dialog & progress ----
        "cancel_download": "❌ Cancel Download",
        "downloading": "Downloading: {model}",
        "download_cancel_title": "Download Cancelled",
        "download_cancelled": "\n❌ Download cancelled.\n",
        "download_done_title": "Download Complete",
        "download_complete": "Model {model} has been successfully downloaded.",
        "download_failed_title": "Download Failed",
        "download_failed_code": "\n❌ Download failed, exit code: {code}\n",

        # ---- Generic errors ----
        "error_title": "Error",
        "download_failed": "Download failed: {error}",
        "model_fetch_failed": "⚠️ Failed to fetch model list, using default list: {error}",
        "local_exe_missing": "Local installer OllamaSetup.exe not found!",
        "local_exe_launch_error": "Cannot launch local installer: {error}",
    },
}

# ------------------------------------------------------------------
# ANSI Escape Code Removal - Keeps Logs Plain Text
# ------------------------------------------------------------------
ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)

# ------------------------------------------------------------------
# main category
# ------------------------------------------------------------------
class OllamaInstallerApp:
    def __init__(self, root: tk.Tk):
        # Basic settings ------------------------------------------------------
        self.root = root
        self.language = "zh"
        self.texts = LANGUAGES[self.language]
        self.current_step = 1
        self.current_frame_name = "welcome"

        # DPI scaling (works with high DPI perception)
        self.root.call("tk", "scaling", 2)

        # Global Fonts - Segoe UI / SiYuan Bold
        self.root.option_add("*Font", ("Segoe UI", 12))

        # Modern Themes: sv-ttk
        try:
            import sv_ttk
            sv_ttk.set_theme("light")
        except ImportError:
            pass  # Can still run if packages are missing

        # Window Title & Size
        self.root.title(self.texts["title"])
        self.root.geometry("700x560")

        # Set window icon (if ico exists)
        ico_path = os.path.join(os.path.dirname(__file__), "ollama.ico")
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception:
                pass

        # Header: step-by-step instructions + language switching
        self.header = ttk.Frame(self.root, padding=(10, 8))
        self.header.pack(fill="x")
        self.step_label = ttk.Label(self.header, text="")
        self.step_label.pack(side="left")
        self.lang_btn = ttk.Button(self.header, text=self.texts["language_toggle"], command=self.toggle_language)
        self.lang_btn.pack(side="right")

        # Main Content Frame - Subsequent Switching
        self.content = ttk.Frame(self.root)
        self.content.pack(expand=True, fill="both")
        self.frames = {}
        self.create_frames()
        self.show_frame("welcome")

        # Bottom status bar
        self.status_var = tk.StringVar()
        self.status = ttk.Label(self.root, relief="sunken", anchor="w", textvariable=self.status_var)
        self.status.pack(fill="x", ipady=2)

    # ------------------------------------------------------------------
    # UI Build
    # ------------------------------------------------------------------
    def create_frames(self):
        self.frames["welcome"] = self.build_welcome()
        self.frames["download"] = self.build_download()
        self.frames["models"] = self.build_models()

    def build_welcome(self):
        f = ttk.Frame(self.content)
        ttk.Label(f, text=self.texts["welcome"], font=("Segoe UI", 14)).pack(pady=40)
        ttk.Button(f, text="中文", width=18, command=lambda: self.start_install("zh")).pack(pady=8)
        ttk.Button(f, text="English", width=18, command=lambda: self.start_install("en")).pack(pady=8)
        return f

    def start_install(self, lang: str):
        """Choose your language and go to the download page"""
        self.set_language(lang)
        self.show_frame("download")

    def build_download(self):
        f = ttk.Frame(self.content, padding=20)
        ttk.Button(
            f, text=self.texts["open_download"], width=44,
            command=lambda: webbrowser.open("https://ollama.com/download/windows")
        ).pack(pady=12)
        ttk.Button(
            f, text=self.texts["local_install"], width=44,
            command=self.install_local_version
        ).pack(pady=8)
        ttk.Button(f, text=self.texts["confirm_downloaded"], width=32, command=lambda: self.show_frame("models")).pack(pady=12)
        ttk.Button(f, text=self.texts["back"], command=lambda: self.show_frame("welcome")).pack(pady=20)
        return f

    def build_models(self):
        f = ttk.Frame(self.content, padding=20)
        # Path Selection + Env Settings
        row = 0
        ttk.Label(f, text=self.texts["select_path"]).grid(row=row, column=0, sticky="w")
        self.path_entry = ttk.Entry(f, width=50)
        self.path_entry.grid(row=row, column=1, pady=4, sticky="w")
        ttk.Button(f, text=self.texts["browse"], command=self.select_folder).grid(row=row, column=2, padx=(8, 0))
        row += 1
        ttk.Button(f, text=self.texts["set_env"], command=self.set_env_var).grid(row=row, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # Model List
        ttk.Label(f, text=self.texts["model_list"]).grid(row=row + 1, column=0, columnspan=3, sticky="w")
        self.model_listbox = tk.Listbox(f, width=66, height=14)
        self.model_listbox.grid(row=row + 2, column=0, columnspan=3, pady=4, sticky="nsew")
        self.model_listbox.bind("<<ListboxSelect>>", self.model_selected)
        f.rowconfigure(row + 2, weight=1)
        f.columnconfigure(1, weight=1)

        ttk.Button(f, text=self.texts["back"], command=lambda: self.show_frame("download")).grid(row=row + 3, column=0, columnspan=3, pady=16)

        # populated model
        self.load_models()
        return f

    # ------------------------------------------------------------------
    # public tool
    # ------------------------------------------------------------------
    def show_frame(self, name):
        for fr in self.frames.values():
            fr.pack_forget()
        self.frames[name].pack(expand=True, fill="both")
        self.current_frame_name = name
        self.current_step = {"welcome": 1, "download": 2, "models": 3}[name]
        self.refresh_header()

    def refresh_header(self):
        self.step_label.config(text=self.texts["step"].format(step=self.current_step))
        self.lang_btn.config(text=self.texts["language_toggle"])
        self.root.title(self.texts["title"])

    def toggle_language(self):
        self.set_language("en" if self.language == "zh" else "zh")

    def set_language(self, lang):
        if lang == self.language:
            return
        self.language = lang
        self.texts = LANGUAGES[self.language]
        # Rebuild all interface text
        for child in self.content.winfo_children():
            child.destroy()
        self.frames.clear()
        self.create_frames()
        # Stay on the same step
        self.show_frame(self.current_frame_name)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.status_var.set(folder)

    def set_env_var(self):
        path = self.path_entry.get()
        if not path:
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        os.system(f'setx {env_var_name} "{path}" /M')
        messagebox.showinfo(self.texts["title"], f"{self.texts['success_env']} {path}")

    # ------------------------------------------------------------------
    # Model List
    # ------------------------------------------------------------------
    def load_models(self):
        specials = ["deepseek-r1:1.5b", "llama3.1:8b"]
        try:
            r = requests.get(model_library_url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            models = []
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("/library/"):
                    m = a["href"].split("/library/")[1]
                    if m and m not in models:
                        models.append(m)
            final = specials + [m for m in models if m not in specials]
        except Exception as e:
            print(self.texts["model_fetch_failed"].format(error=e))
            fallback = ["llama3", "phi3", "mistral", "deepseek-coder", "codellama"]
            final = specials + fallback
        self.model_listbox.delete(0, tk.END)
        for m in final:
            self.model_listbox.insert(tk.END, m)

    def model_selected(self, _):
        if not self.path_entry.get():
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        idxs = self.model_listbox.curselection()
        if not idxs:
            return
        model = self.model_listbox.get(idxs[0])
        if messagebox.askyesno(self.texts["title"], f"{self.texts['confirm_pull']} {model}?"):
            self.pull_model(model)

    # ------------------------------------------------------------------
    # Model Download
    # ------------------------------------------------------------------
    def pull_model(self, model):
        def worker():
            try:
                startupinfo = None
                if sys.platform == "win32":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                proc = subprocess.Popen(
                    ["ollama", "pull", model],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace",
                    startupinfo=startupinfo,
                )
                self.show_download_window(proc, model)
            except Exception as e:
                messagebox.showerror(self.texts["error_title"], self.texts["download_failed"].format(error=e))
        threading.Thread(target=worker, daemon=True).start()

    def show_download_window(self, proc, model):
        win = tk.Toplevel(self.root)
        win.title(self.texts["downloading"].format(model=model))
        win.geometry("660x460")

        ttk.Label(win, text=model, font=("Segoe UI", 13, "bold")).pack(pady=(12, 4))

        bar_style = ttk.Style(win)
        bar_style.configure("GreenPB.Horizontal.TProgressbar", troughcolor="#E0E0E0", background="#34C759")
        pbar = ttk.Progressbar(win, mode="determinate", maximum=100, length=540, style="GreenPB.Horizontal.TProgressbar")
        pbar.pack(pady=8)

        log = st.ScrolledText(win, wrap=tk.WORD, height=18)
        log.pack(expand=True, fill=tk.BOTH, padx=10)

        cancel_btn = ttk.Button(win, text=self.texts["cancel_download"])
        cancel_btn.pack(pady=6)

        cancelled = False
        steps = ["pulling manifest", "pulling layers", "extracting", "verifying", "success"]
        done_steps = set()

        def cancel():
            nonlocal cancelled
            cancelled = True
            try:
                proc.terminate()
            except Exception:
                pass
            cancel_btn.state(["disabled"])
            win.title(self.texts["download_cancel_title"])
            log.insert(tk.END, self.texts["download_cancelled"])
            pbar.stop()
        cancel_btn.config(command=cancel)

        def reader():
            for line in proc.stdout:
                if cancelled:
                    break
                txt = strip_ansi(line)
                log.insert(tk.END, txt)
                log.see(tk.END)
                for s in steps:
                    if s in txt and s not in done_steps:
                        done_steps.add(s)
                        pbar["value"] = int(len(done_steps) / len(steps) * 100)
                        break
            proc.wait()
            cancel_btn.state(["disabled"])
            if cancelled:
                return
            if proc.returncode == 0:
                pbar["value"] = 100
                log.insert(tk.END, f"\n✅ {self.texts['download_complete'].format(model=model)}\n")
                win.title(self.texts["download_done_title"])
                messagebox.showinfo(self.texts["download_done_title"], self.texts["download_complete"].format(model=model))
            else:
                log.insert(tk.END, self.texts["download_failed_code"].format(code=proc.returncode))
                win.title(self.texts["download_failed_title"])
        threading.Thread(target=reader, daemon=True).start()

    # ------------------------------------------------------------------
    # local installer
    # ------------------------------------------------------------------
    def install_local_version(self):
        exe = os.path.join(os.path.dirname(__file__), "OllamaSetup.exe")
        if not os.path.exists(exe):
            messagebox.showerror(self.texts["title"], self.texts["local_exe_missing"])
            return
        try:
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen([exe], startupinfo=startupinfo)
        except Exception as e:
            messagebox.showerror(self.texts["title"], self.texts["local_exe_launch_error"].format(error=e))

# ------------------------------------------------------------------
# Launch Entrance
# ------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaInstallerApp(root)
    root.mainloop()
