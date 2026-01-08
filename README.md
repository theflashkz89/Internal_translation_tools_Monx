# Internal Translation Tools

An intelligent translation and document processing tool built with Streamlit. This application provides multiple translation services and document utilities powered by AI.

## Features

### 📝 Online Text Translation
- Translate text in real-time using DeepL API
- Support for multiple languages: Chinese, English, Italian, German
- Fast and accurate translation results

### 📂 Document File Translation
- Upload Word (.docx) or PDF files for translation
- Preserves original document formatting
- Supports batch translation of document paragraphs
- Progress tracking during translation

### 📊 PPT Generation
- Convert structured text content into PowerPoint presentations
- Automatic slide creation with titles and bullet points
- Easy-to-use text format for quick PPT generation

### ✉️ Email Assistant
- AI-powered email draft generation
- Multiple email types: Business, Thank You, Request, Notification, Reply
- Tone options: Formal, Friendly, Concise, Polite
- Language support: Chinese, English, Italian
- **Italian Formal**: Automatically uses formal Italian address (Lei form) when language is Italian and tone is Formal

### 📧 Email Proofreading
- AI-powered email proofreading and editing
- Two proofreading modes:
  - **Grammar Correction Only**: Fixes grammar, spelling, and punctuation errors while preserving original style
  - **Polish & Improve**: Enhances expression, fluency, and professionalism in addition to fixing errors
- Language options: Chinese, English, Italian
- Tone adjustments: Friendly, Formal, Concise
- Custom terminology support
- Side-by-side comparison of original and proofread versions
- Content limit: 5,000 characters
- **Italian Formal**: Automatically uses formal Italian address (Lei form) when language is Italian and tone is Formal

## Requirements

- Python 3.11+
- See `requirements.txt` for dependencies

## Installation

1. Clone the repository:
```bash
git clone https://github.com/theflashkz89/Internal-translation-tools.git
cd Internal-translation-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
   - DeepL API Key (for translations)
   - DeepSeek API Key (for AI features)
   
   See `API_KEY配置指南.md` for detailed configuration instructions.

4. Run the application:
```bash
streamlit run app.py
```

Or use the packaged executable:
```bash
python run_app.py
```

## Configuration

API keys can be configured in two ways:
1. Environment variables: `DEEPL_API_KEY` and `DEEPSEEK_API_KEY`
2. Streamlit secrets: Create `.streamlit/secrets.toml` file

See `API_KEY配置指南.md` for detailed instructions.

## Building Executable

The project includes PyInstaller spec files for creating standalone executables:
- `Monx Internal Tools V1.51.spec` (latest version)

Build using:
```bash
pyinstaller "Monx Internal Tools V1.51.spec"
```

## Project Structure

```
├── app.py                 # Main application entry point
├── utils.py               # Core utility functions
├── ai_service.py          # AI service integration
├── config.py              # Configuration management
├── run_app.py             # Executable launcher
├── pages/                 # Additional page modules
├── _pages_backup/         # Backup page files
└── requirements.txt       # Python dependencies
```

## Version

Current version: **v2.2 Stable**

### Changelog

#### v2.2 (Latest)
- ✨ Added Email Proofreading feature
  - Grammar correction and content polishing modes
  - Side-by-side comparison view
  - Automatic configuration change detection
  - Character limit: 5,000 characters
  - Support for custom terminology

#### v2.1
- Initial stable release
- Online text translation
- Document file translation
- PPT generation
- Email assistant

## License

This project is for internal use only.

## Support

For issues or questions, please open an issue on GitHub.
