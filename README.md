# Ollama Quick Installer for Windows

A user-friendly graphical installer for [Ollama](https://ollama.com) on Windows, featuring:

- 📦 One-click model selection and downloading
- 🌐 Language toggle: English / 中文
- ⚙️ Automatic environment variable configuration (`OLLAMA_MODELS`)
- 🧾 Legacy installer support for offline use
- 🧑‍💻 Open-source and community-friendly

## 🚀 Why This Project?

While Ollama provides powerful local LLM capabilities, installing it on Windows still involves:

- Manually downloading the installer
- Manually configuring environment variables
- Running `ollama pull` via command line for each model

This tool simplifies the entire process through a clean GUI, helping beginners and researchers get started faster.

## 🖼️ Features

- Multi-step wizard interface (Welcome → Install Ollama → Select and Pull Models)
- Model list auto-fetched from [Ollama Library](https://ollama.com/library)
- Model download with progress and cancel options
- Environment variable (`OLLAMA_MODELS`) set automatically
- Optionally run bundled `OllamaSetup.exe` for offline/legacy use
- Fully localized in English and Simplified Chinese

## 🔧 Installation

1. Download the latest installer from the [Releases](https://github.com/EthanYixuanMi/ollama-windows-installer/releases) page.
2. Run the `.exe` and follow the on-screen steps.
3. You're ready to use `ollama` with your selected models!

## 💡 Screenshot

![screenshot](screenshot.png) <!-- You can replace this with your actual screenshot -->

## 🔄 Versioning

We publish versioned releases for every major update. See the [Releases](https://github.com/EthanYixuanMi/ollama-windows-installer/releases) section for changelogs and downloads.

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo, submit pull requests, or open issues.

```bash
git clone https://github.com/EthanYixuanMi/ollama-windows-installer.git
