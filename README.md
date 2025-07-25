# Ollama Quick Installer for Windows

[![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)](#)
[![Python](https://img.shields.io/badge/Built%20with-Python%203.8+-yellow.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Author](https://img.shields.io/badge/Author-Yixuan%20Mi-blue.svg)](https://github.com/EthanYixuanMi)
[![Release](https://img.shields.io/github/v/release/EthanYixuanMi/ollama-windows-installer?include_prereleases&label=Latest%20Release)](https://github.com/EthanYixuanMi/ollama-windows-installer/releases)
[![Issues](https://img.shields.io/github/issues/EthanYixuanMi/ollama-windows-installer.svg)](https://github.com/EthanYixuanMi/ollama-windows-installer/issues)
[![Stars](https://img.shields.io/github/stars/EthanYixuanMi/ollama-windows-installer.svg?style=social)](https://github.com/EthanYixuanMi/ollama-windows-installer/stargazers)


A user-friendly graphical installer for [Ollama](https://ollama.com) on Windows.

---

## ✨ Features

- 🪟 Intuitive 3-step GUI  
  1. Welcome (language selection)  
  2. Ollama installer download (online or local version)  
  3. Model selection and download  
- 🌐 Supports English / 简体中文 language toggle  
- 📦 Real-time model list fetching from [ollama.com/library](https://ollama.com/library)  
- 🔽 One-click model download using `ollama pull <model>`  
- 📊 Download progress bar and step tracking (pull → extract → verify)  
- ❌ Cancel model download at any time  
- ⚙️ Auto setup of the `OLLAMA_MODELS` environment variable  
- 💽 Optional installer: bundled legacy version of `OllamaSetup.exe`

---

## 🎯 Motivation

Installing Ollama on Windows typically requires:
- Visiting the website to download the installer
- Manually configuring environment variables
- Using the terminal to pull models

This tool streamlines the whole process via a GUI and lets you:
- Choose language and model storage path
- Install Ollama either from the official website or a local setup file
- Pull models with one click
- Monitor download status interactively

---

## 📦 Installation

1. Download the latest `.exe` release from the [Releases](https://github.com/EthanYixuanMi/ollama-windows-installer/releases) page.  
2. Double-click to launch and follow the 3-step interface.  
   - You may choose to install Ollama from the website or use the built-in `OllamaSetup.exe` installer.  
3. After setup, select your model storage path and download models interactively.

> 💡 Note: Internet access is required to fetch the model list or pull models.

---

## 📷 Screenshots

<img width="442" height="233" alt="image" src="https://github.com/user-attachments/assets/518e50f4-b365-4d8e-82ee-30be43b6bbe6" />

---

## 🛠 Planned Improvements

We plan to gradually enhance the installer with:

- 🎨 Improved UI/UX (e.g. animations, styling, icons)
- 🧩 Model update check / version control
- 📁 Integrated offline model support
- 📜 Log file export after download
- 🛠 Better error handling & platform compatibility

Feel free to suggest features via [Issues](https://github.com/EthanYixuanMi/ollama-windows-installer/issues) or contribute via PR!

---

## 🚀 Development

### Prerequisites

- Python 3.8+
- `pip install -r requirements.txt`

### Build (Windows .exe)

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "OllamaSetup.exe;." ollama_installer.py
