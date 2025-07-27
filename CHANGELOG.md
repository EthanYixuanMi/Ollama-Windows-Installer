# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.2.0] - 2025-07-27
### Added
- 🌐 **Extended multilingual support**: Added 16 new localized strings covering UI elements, error messages, and installation prompts
- 🔤 **Featured models**: Added "deepseek-r1:1.5b" and "llama3.1:8b" as fixed-size models displayed at top of model list
- 📍 **Improved model list logic**:
  - Featured models always appear first in the list
  - Fallback list includes featured models when network fetch fails

### Changed
- ♻️ **Code restructuring**:
  - Modularized UI creation into separate methods
  - Separated model download functionality from UI operations
- 📝 **Enhanced error handling**:
  - Unified error messages with multilingual support
  - Added existence check for local installer EXE

### Fixed
- 🚫 **Progress bar completion**:
  - Added "success" step to complete the final 20% of progress
  - Fixed step counting algorithm (5 steps → 100%)
- ✂️ **Terminal log sanitization**: Implemented ANSI escape code filtering for cleaner output

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
