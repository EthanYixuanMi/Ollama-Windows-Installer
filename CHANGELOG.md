# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.1.0] - 2025-07-22

### Added
- 📦 Option to install Ollama from a local setup file (`OllamaSetup.exe`)
- ➕ New button in Step 2 interface for installing legacy version
- 🪟 Removed unnecessary terminal window using `--windowed` in PyInstaller

### Improved
- UI text localization for new install option (EN/中文)
- README and build instructions updated

### Fixed
- No more terminal popup on `.exe` launch

---

## [v1.0.0] - 2025-07-21

### Added
- 🎉 Initial public release of **Ollama Quick Installer for Windows**
- Full GUI with Tkinter (3-step interface):
  - Welcome screen with language selection (English / 中文)
  - Ollama website link to download the official installer
  - Model list fetched live from https://ollama.com/library
- 📂 Model path selection and auto-setup of `OLLAMA_MODELS` environment variable
- 📥 Model download via `ollama pull` with:
  - Realtime terminal log display
  - Progress bar based on pull steps (manifest, layers, extracting, verifying)
  - Cancel download functionality
- 🧩 Fallback to default model list if network fetch fails
- 🪟 Clean, DPI-aware layout (600x500 fixed size)

### Known Limitations
- No dark mode or `.ico` integration yet
- Pull logs shown only in a popup window (not stored)
- One model download at a time (no queue support)

---
