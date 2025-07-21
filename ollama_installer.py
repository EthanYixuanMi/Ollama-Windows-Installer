import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import tkinter.scrolledtext as st
import shutil
import tempfile

env_var_name = "OLLAMA_MODELS"
model_library_url = "https://ollama.com/library"

LANGUAGES = {
    "zh": {
        "title": "Ollama 快速安装器",
        "welcome": "欢迎使用 Ollama 快速安装器，请选择语言：",
        "step": "当前步骤：第 {step} 步，共 3 步",
        "open_download": "打开 Ollama 官网下载安装包",
        "legacy_download": "使用内置旧版本 Ollama 安装包",
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
        "language_toggle": "切换语言",
        "error_legacy": "无法启动内置安装程序：{error}"
    },
    "en": {
        "title": "Ollama Quick Installer",
        "welcome": "Welcome to the Ollama Quick Installer. Please select a language:",
        "step": "Current Step: {step} of 3",
        "open_download": "Open Ollama website to download",
        "legacy_download": "Use bundled legacy Ollama installer",
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
        "language_toggle": "Toggle Language",
        "error_legacy": "Failed to launch legacy installer: {error}"
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
        download_btn.pack(pady=20)

        legacy_btn = tk.Button(frame, text=self.texts["legacy_download"], width=30, command=self.run_legacy_installer)
        legacy_btn.pack(pady=5)

        confirm_btn = tk.Button(frame, text=self.texts["confirm_downloaded"], width=30,
                                command=lambda: self.show_frame("models"))
        confirm_btn.pack(pady=10)

        back_btn = tk.Button(frame, text=self.texts["back"], command=lambda: self.show_frame("welcome"))
        back_btn.pack(pady=20)

        return frame

    def run_legacy_installer(self):
        try:
            # 检查是否已安装 Ollama
            if shutil.which("ollama"):
                proceed = messagebox.askyesno(
                    self.texts["title"],
                    "检测到您的系统已安装 Ollama。\n仍然要继续运行旧版本安装包吗？" if self.language == "zh"
                    else "Ollama is already installed on your system.\nDo you still want to run the legacy installer?"
                )
                if not proceed:
                    return

            # 将 OllamaSetup.exe 解压到临时目录并执行
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, "OllamaSetup.exe")
            with open(installer_path, "wb") as f_out:
                with open(os.path.join(getattr(sys, '_MEIPASS', '.'), "OllamaSetup.exe"), "rb") as f_in:
                    shutil.copyfileobj(f_in, f_out)
            subprocess.Popen(installer_path, shell=True)
        except Exception as e:
            messagebox.showerror(self.texts["title"], self.texts["error_legacy"].format(error=e))

