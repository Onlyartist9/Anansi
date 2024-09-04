# Anansi - Anki Deck Creation Assistant

Anansi is your assistant for creating Anki decks. You can upload files in various formats (txt, pdf, docx, csv, html, epub) or ask for a deck of questions on a specific subject without uploading a file. After generating the question-answer pairs, you can download the text file and import it into Anki.

## Features

- Upload files in various formats (txt, pdf, docx, csv, html, epub)
- Generate question-answer pairs from the uploaded text
- Import the generated text file into Anki

## Installation

### Using Python

1. Clone the repository and change directory into the cloned repo:
    ```bash
    git clone https://github.com/onlyartist9/anansi.git
    cd anansi
    ```
    
2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

4. Open your browser and go to:
    ```bash
    http://localhost:8501
    ```

### Using Docker

1. Clone the repository and change directory into the cloned repo:
    ```bash
    git clone https://github.com/onlyartist9/anansi.git
    cd anansi
    ```

2. Build the Docker image:
    ```bash
    docker build -t anansi .
    ```

3. Run the Docker container:
    ```bash
    docker run -p 8501:8501 anansi
    ```

4. Open your browser and go to:
    ```bash
    http://localhost:8501
    ```

# On output.

Claude is imperfect and sometimes its responses will vary often, producing improperly formatted output. These are often fixed with some minor adjustments to the text file. See [this](https://docs.ankiweb.net/importing/text-files.html#:~:text=Any%20plain%20text%20file%20that%20contains%20fields).


# On the benefits and utility of Spaced Repetition

There's not enough good to be said about the benefits of Spaced Repetition. It isn't simply a system for memorization but for familiarizing with practically anything one wants to get accustomed to. The best overview of the subject comes from Gwern who provides an overview of the preexisting research on the topic [here](https://gwern.net/spaced-repetition).