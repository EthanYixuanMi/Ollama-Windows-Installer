# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.0.0] - 2025-07-21

### Added
- 🎉 Initial release of **Ollama Quick Installer for Windows**
- GUI-based multi-step installer using Python and Tkinter
- Language selection (English / 中文)
- Step-by-step interface:
  - Step 1: Welcome page with language toggle
  - Step 2: Ollama installer download
  - Step 3: Model list and installation
- 🧰 Environment variable (`OLLAMA_MODELS`) setup automation
- 🌐 Real-time fetching of available models from [ollama.com/library](https://ollama.com/library)
- 📥 Model downloading via `ollama pull <model>` with progress log and cancel button
- 📦 Legacy installer support (bundled `OllamaSetup.exe`), with installed check
- User-friendly error handling and confirmation dialogs
- Built-in localized text dictionary for future i18n extension

### Known Limitations
- No built-in model version filtering (only fetches latest list)
- Currently not supporting model download retry on failure
- Requires admin permission for environment variable setup (expected behavior)

---

