# Anansi - Anki Deck Creation Assistant

Anansi is your assistant for creating Anki decks. You can upload files in various formats (txt, pdf, docx, csv, html, epub) or ask for a deck of questions on a specific subject without uploading a file. After generating the question-answer pairs, you can download the text file and import it into Anki.

## Features

- Upload files in various formats (txt, pdf, docx, csv, html, epub)
- Generate question-answer pairs from the uploaded text
- Import the generated text file into Anki

## Installation

1. Clone the repository:
```bash
    git clone https://github.com/onlyartist9/anansi.git
    cd anansi
```
    
2. Install the required libraries:
```bash
    pip install -r requirements.txt
```
3. Set up your environment variables:
```bash
export ANTHROPIC_API_KEY=your_api_key
```
4. Run the Streamlit app:
```bash
streamlit run app.py
```
5. Open your browser and go to:
```bash
http://localhost:8501
```




