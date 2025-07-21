# Ollama Quick Installer for Windows

A user-friendly graphical installer for [Ollama](https://ollama.com) on Windows.

---

## ✨ Features

- 🪟 Intuitive 3-step GUI
  1. Welcome (language selection)
  2. Ollama official installer download
  3. Model selection and download
- 🌐 Supports English / 简体中文 language toggle
- 📦 Real-time model list fetching from [ollama.com/library](https://ollama.com/library)
- 🔽 One-click model download using `ollama pull <model>`
- 📊 Download progress bar and step tracking (pull → extract → verify)
- ❌ Cancel model download at any time
- ⚙️ Auto setup of the `OLLAMA_MODELS` environment variable

---

## 🎯 Motivation

Installing Ollama on Windows typically requires:
- Visiting the website to download the installer
- Manually configuring environment variables
- Using the terminal to pull models

This tool streamlines the whole process via a GUI and lets you:
- Choose language and model storage path
- Pull models with one click
- Monitor download status interactively

---

## 📦 Installation

1. Download the latest `.exe` release from the [Releases](https://github.com/EthanYixuanMi/ollama-quick-installer/releases) page.
2. Double-click to launch and follow the 3-step interface.
3. Enjoy Ollama with your selected models.

> 💡 You must install the official Ollama binary during Step 2 to use model pulling.

---

## 📷 Screenshots

_Add screenshots here (e.g., welcome page, model download progress, etc.)_

---

## 🚀 Development

### Prerequisites

- Python 3.8+
- `pip install -r requirements.txt`

### Build (Windows .exe)

```bash
pyinstaller --noconfirm --onefile --windowed main.py
