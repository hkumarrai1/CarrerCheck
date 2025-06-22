# Resume ATS Checker (Offline)

A powerful, fully offline tool to analyze your resume against job descriptions using ATS-style keyword and semantic matching, NLP section extraction, and live editing.

## Features

- Parse PDF, DOCX, and TXT resumes and job descriptions
- Keyword and semantic similarity scoring
- Live resume editor with instant feedback
- NLP-based extraction of skills, education, and experience
- Job description input via file, clipboard, manual paste, or screenshot+OCR
- Actionable improvement suggestions

## Installation

1. Clone or download this repository.
2. Install Python 3.9+.
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Download spaCy English model:
   ```sh
   python -m spacy download en_core_web_sm
   ```
5. Install Tesseract OCR (for screenshot OCR):
   - Windows: Download from https://github.com/tesseract-ocr/tesseract
   - Add Tesseract to your system PATH.

## Usage

### Web App (Recommended)

```sh
streamlit run streamlit_app.py
```

- Open the link in your browser.
- Upload or paste your resume and job description.
- Edit your resume live and see instant feedback!

### Command Line

```sh
python app.py
```

## Notes

- All processing is local/offline.
- For best results, use clear, well-formatted resumes and job descriptions.
- For OCR, make sure Tesseract is installed and in your PATH.

## License

MIT License
