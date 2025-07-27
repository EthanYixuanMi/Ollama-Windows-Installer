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

env_var_name = "OLLAMA_MODELS"
model_library_url = "https://ollama.com/library"

LANGUAGES = {
    "zh": {
        # ---- Window & Navigation ----
        "title": "Ollama 快速安装器",
        "welcome": "欢迎使用 Ollama 快速安装器，请选择语言：",
        "step": "当前步骤：第 {step} 步，共 3 步",
        "back": "返回",
        "language_toggle": "切换语言",

        # ---- Download page ----
        "open_download": "打开 Ollama 官网下载安装包",
        "confirm_downloaded": "我已下载完成",
        "local_install": "📦 安装本地版本",

        # ---- Model page ----
        "select_path": "请选择模型存储路径：",
        "browse": "浏览...",
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
        "language_toggle": "Toggle Language",

        # ---- Download page ----
        "open_download": "Open Ollama website to download",
        "confirm_downloaded": "I have completed the download",
        "local_install": "📦 Install Local Version",

        # ---- Model page ----
        "select_path": "Please select model storage path:",
        "browse": "Browse...",
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


def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


class OllamaInstallerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.language = "zh"
        self.texts = LANGUAGES[self.language]
        self.models = []
        self.current_step = 1

        self.root.geometry("600x500")
        self.root.title(self.texts["title"])

        # ---- Header (step indicator + language toggle) ----
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill="x")
        self.step_label = tk.Label(self.header_frame, text="", font=("Arial", 10), anchor="w")
        self.step_label.pack(side="left", padx=10, pady=5)
        self.lang_btn = tk.Button(self.header_frame, text=self.texts["language_toggle"], command=self.toggle_language)
        self.lang_btn.pack(side="right", padx=10)

        # ---- Main content frame ----
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill="both")
        self.frames = {}
        self.create_frames()
        self.show_frame("welcome")

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
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

    def show_frame(self, name: str):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        self.current_frame_name = name
        self.current_step = {"welcome": 1, "download": 2, "models": 3}.get(name, 1)
        self.update_header()

    # ------------------------------------------------------------------
    # Frame creators
    # ------------------------------------------------------------------
    def create_welcome_frame(self):
        frame = tk.Frame(self.content_frame)
        label = tk.Label(frame, text=self.texts["welcome"], font=("Arial", 14))
        label.pack(pady=40)

        tk.Button(frame, text="中文", width=15, command=lambda: self.set_language("zh")).pack(pady=10)
        tk.Button(frame, text="English", width=15, command=lambda: self.set_language("en")).pack(pady=10)
        return frame

    def create_download_frame(self):
        frame = tk.Frame(self.content_frame)

        tk.Button(
            frame,
            text=self.texts["open_download"],
            font=("Arial", 12),
            height=2,
            width=40,
            command=lambda: webbrowser.open("https://ollama.com/download/windows"),
        ).pack(pady=20)

        # Local version installer button
        tk.Button(
            frame,
            text=self.texts["local_install"],
            font=("Arial", 12),
            height=2,
            width=40,
            command=self.install_local_version,
        ).pack(pady=10)

        tk.Button(frame, text=self.texts["confirm_downloaded"], width=30, command=lambda: self.show_frame("models")).pack(pady=10)
        tk.Button(frame, text=self.texts["back"], command=lambda: self.show_frame("welcome")).pack(pady=20)
        return frame

    def create_model_frame(self):
        frame = tk.Frame(self.content_frame)

        tk.Label(frame, text=self.texts["select_path"]).pack()
        self.path_entry = tk.Entry(frame, width=50)
        self.path_entry.pack()
        tk.Button(frame, text=self.texts["browse"], command=self.select_folder).pack()
        tk.Button(frame, text=self.texts["set_env"], command=self.set_env_var).pack(pady=10)

        tk.Label(frame, text=self.texts["model_list"]).pack(pady=5)
        self.model_listbox = tk.Listbox(frame, width=50, height=15)
        self.model_listbox.pack()
        self.model_listbox.bind("<<ListboxSelect>>", self.model_selected)

        tk.Button(frame, text=self.texts["back"], command=lambda: self.show_frame("download")).pack(pady=10)

        self.load_models()
        return frame

    # ------------------------------------------------------------------
    # Language / path helpers
    # ------------------------------------------------------------------
    def set_language(self, lang: str):
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

    # ------------------------------------------------------------------
    # Model list handling
    # ------------------------------------------------------------------
    def load_models(self):
        self.models = self.fetch_online_models()
        self.model_listbox.delete(0, tk.END)
        for model in self.models:
            self.model_listbox.insert(tk.END, model)

    def fetch_online_models(self):
        """
        Fetch the model list from the Ollama library page **and** always prepend two
        fixed-size models so they appear at the very top of the listbox. Clicking
        them follows the same installation logic (`ollama pull <model>`).
        """
        specials = ["deepseek-r1:1.5b", "llama3.1:8b"]
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
            # 确保特定模型位于最上方，且不重复
            final_list = specials + [m for m in model_list if m not in specials]
            return final_list
        except Exception as e:
            print(self.texts["model_fetch_failed"].format(error=e))
            fallback = ["llama3", "phi3", "mistral", "deepseek-coder", "codellama"]
            return specials + fallback

    # ------------------------------------------------------------------
    # Model download flow
    # ------------------------------------------------------------------
    def model_selected(self, event):
        if not self.path_entry.get():
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        selection = self.model_listbox.curselection()
        if not selection:
            return
        selected = self.model_listbox.get(selection[0])
        if messagebox.askyesno(self.texts["title"], f"{self.texts['confirm_pull']} {selected}?"):
            self.pull_model(selected)

    def pull_model(self, model_name: str):
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
                    encoding="utf-8",
                    errors="replace",
                    startupinfo=startupinfo,
                )
                self.show_download_window(process, model_name)
            except Exception as e:
                messagebox.showerror(self.texts["error_title"], self.texts["download_failed"].format(error=e))

        threading.Thread(target=run_pull, daemon=True).start()

    def show_download_window(self, process: subprocess.Popen, model_name: str):
        win = tk.Toplevel(self.root)
        win.title(self.texts["downloading"].format(model=model_name))
        win.geometry("600x400")

        # Progress bar styling
        style = ttk.Style(win)
        style.theme_use("default")
        style.configure(
            "green.Horizontal.TProgressbar",
            troughcolor="white",
            bordercolor="black",
            background="green",
            lightcolor="green",
            darkcolor="green",
        )

        progress = ttk.Progressbar(win, orient="horizontal", length=500, mode="determinate", style="green.Horizontal.TProgressbar", maximum=100)
        progress.pack(pady=5)

        log_area = st.ScrolledText(win, wrap=tk.WORD)
        log_area.pack(expand=True, fill=tk.BOTH)

        cancel_btn = tk.Button(win, text=self.texts["cancel_download"], fg="red")
        cancel_btn.pack(pady=5)

        steps = ["pulling manifest", "pulling layers", "extracting", "verifying", "success"]
        completed_steps = set()
        cancelled = False

        # ------------------------------------------------------------------
        # Cancellation logic
        # ------------------------------------------------------------------
        def cancel_download():
            nonlocal cancelled
            cancelled = True
            try:
                process.terminate()
            except Exception:
                pass
            progress.stop()
            log_area.insert(tk.END, self.texts["download_cancelled"])
            log_area.see(tk.END)
            cancel_btn.config(state=tk.DISABLED)
            win.title(self.texts["download_cancel_title"])

        cancel_btn.config(command=cancel_download)

        # ------------------------------------------------------------------
        # Read subprocess output and update progress
        # ------------------------------------------------------------------
        def read_output():
            nonlocal cancelled
            for line in process.stdout:
                if cancelled:
                    break
                clean_line = strip_ansi_codes(line)
                log_area.insert(tk.END, clean_line)
                log_area.see(tk.END)

                for step in steps:
                    if step in clean_line and step not in completed_steps:
                        completed_steps.add(step)
                        percent = int(len(completed_steps) / len(steps) * 100)
                        progress["value"] = percent
                        break

            process.wait()
            cancel_btn.config(state=tk.DISABLED)

            if cancelled:
                return

            if process.returncode == 0:
                progress["value"] = 100
                log_area.insert(tk.END, f"\n✅ {self.texts['download_complete'].format(model=model_name)}\n")
                log_area.see(tk.END)
                messagebox.showinfo(self.texts["download_done_title"], self.texts["download_complete"].format(model=model_name))
                win.title(self.texts["download_done_title"])
            else:
                log_area.insert(tk.END, self.texts["download_failed_code"].format(code=process.returncode))
                log_area.see(tk.END)
                win.title(self.texts["download_failed_title"])

        threading.Thread(target=read_output, daemon=True).start()

    # ------------------------------------------------------------------
    # Local installer launcher
    # ------------------------------------------------------------------
    def install_local_version(self):
        try:
            exe_path = os.path.join(os.path.dirname(__file__), "OllamaSetup.exe")
            if not os.path.exists(exe_path):
                messagebox.showerror(self.texts["title"], self.texts["local_exe_missing"])
                return

            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.Popen([exe_path], shell=True, startupinfo=startupinfo)
        except Exception as e:
            messagebox.showerror(self.texts["title"], self.texts["local_exe_launch_error"].format(error=e))


if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaInstallerApp(root)
    root.mainloop()
