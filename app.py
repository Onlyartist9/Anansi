import streamlit as st
import anthropic
import chardet
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import fitz 
import docx
import uuid
import tempfile

MODEL = "claude-3-haiku-20240307"
MAX_TOKENS = 4096
SYSTEM ="""
# Anki Deck Creation Assistant

You are Anansi, the knowledge deity and assistant to mortals who need help designing and creating their Anki decks. When creating Anki decks, adhere to the following guidelines:

## File Format Guidelines

1. **Separator**: Use semicolons (;) as separators throughout the file.

2. **Fields**: Each line represents a card. Fields are separated by the chosen separator. At minimum, include a "Front" and "Back" field.

3. **Field Order**: The first line of the file should be a header row specifying field names, e.g., "Front;Back;Tags".

4. **HTML Formatting**: You can use basic HTML tags for formatting within fields. Common tags include:
   - `<b>bold</b>`
   - `<i>italic</i>`
   - `<u>underline</u>`
   - `<br>` for line breaks

5. **Tags**: Include tags in a separate field named "Tags". Separate multiple tags with spaces.

6. **Escaping**: If your chosen separator appears in the content, enclose the entire field in double quotes (").

7. **Comments**: Lines starting with '#' are treated as comments and ignored during import.

## Example Anki Text File:

Front;Back;Tags What is a p-value in statistics?;A p-value is the probability of obtaining test results at least as extreme as the observed results, assuming the null hypothesis is true.;statistics probability What is the mean of the data set {2, 4, 6, 8, 10}?;The mean is 6.;statistics mean What is the probability of rolling a 3 on a fair six-sided die?;The probability is 1/6.;probability dice What does HTML stand for?;HTML stands for <b>H</b>yper<b>T</b>ext <b>M</b>arkup <b>L</b>anguage.;computing web “What is Anki’s default separator for text imports?”;Anki’s default separator for text imports is the tab character.;anki software

## Response Format

When asked to create an Anki deck, provide only the valid file content, without any additional explanation or commentary. Follow these steps:

1. Begin with a header row specifying field names.
2. Use semicolons as the default separator unless otherwise specified.
3. Include at least "Front" and "Back" fields for each card.
4. Add a "Tags" field if tags are relevant.
5. Ensure all lines (except comments) have the same number of fields.
6. Use proper escaping for fields containing the separator character.
7. Implement appropriate HTML formatting for emphasis or structure when needed.

## Important Note

Always return the file content in a format ready for direct import into Anki, with no surrounding explanation or markdown code blocks. Stick to the response format.
"""


def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    file.seek(0)  # Reset file pointer to the beginning
    return encoding if encoding else 'utf-8'

def read_epub(file):
    # Create a unique UUID for the file
    unique_filename = f"{uuid.uuid4()}.epub"
    
    # Create a temporary file with the .epub extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
        tmp_file.write(file.read())
        tmp_file_path = tmp_file.name
    
    # Read the EPUB file from the temporary file
    book = epub.read_epub(tmp_file_path)
    
    text = ''
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text += item.get_content().decode('utf-8')
    
    return text

def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = []
    for page in doc:
        text.append(page.get_text())
    return '\n'.join(text)

def read_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    return soup.get_text()

def read_docx(file):
    doc = docx.Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

def generate_questions_from_text(text, n, user_input, client, model, max_tokens, system):
    prompt = f"{user_input}. \n\nGenerate {n} distinct front-back pairs based on the following text:\n\n{text}"
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt},
            {"role":"assistant","content": f"Here are {n} distinct front-back pairs based on what you requested:"}
        ],
    )
    return response.content[0].text if response else 'No response from API'

# Function to generate questions without text
def generate_questions(n, user_input, client, model, max_tokens, system):
    prompt = f"{user_input}\n\nGenerate {n} distinct front-back pairs."
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.content[0].text if response else 'No response from API'

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

st.title("Anansi")

st.sidebar.title("About")
st.sidebar.info("""
Anansi is your assistant for creating Anki decks. You can upload files in various formats (txt, pdf, docx, csv, html, odt, rtf, epub) or ask for a deck of questions on a specific subject without uploading a file. After generating the question-answer pairs, you can download the text file and import it into Anki.
""")

st.sidebar.title("Instructions")
st.sidebar.info("""
1. **Enter API Key**: Provide your Anthropic API key in the input field.
2. **Upload a File**: You can upload files in various formats (txt, pdf, docx, csv, html, epub) with a maximum size of 10MB.
3. **Generate Questions**: If no file is uploaded, you can ask for a deck of questions on a specific subject.
4. **Download the File**: After generating the question-answer pairs, download the text file.
5. **Import to Anki**: Open Anki, go to `File` -> `Import`, select the downloaded text file, map the fields, and import the cards into your deck.
""")

# Input for API key
api_key = st.text_input("Enter your Anthropic API key", type="password")

uploaded_file = st.file_uploader("Upload a file (max 20MB)", type=["txt", "pdf", "docx", "csv", "html", "epub"])
num_questions = st.number_input("How many question/answer pairs do you need?", min_value=5, max_value=100, value=10)
user_input = st.text_area("How can I help you?", "",placeholder="I need to test my knowledge on CUDA kernel implementations.")

if st.button("Generate"):
    if api_key:
        client = anthropic.Anthropic(api_key=api_key)
        model = MODEL
        max_tokens = MAX_TOKENS
        system = SYSTEM

        if uploaded_file is not None:
            if uploaded_file.size > 20 * 1024 * 1024:
                st.error("File size exceeds 10MB. Please upload a smaller file.")
            else:
                if uploaded_file.type == "application/epub+zip":
                    text = read_epub(uploaded_file)
                elif uploaded_file.type == "application/pdf":
                    text = read_pdf(uploaded_file)
                elif uploaded_file.type in ["text/html", "application/xhtml+xml"]:
                    text = read_html(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = read_docx(uploaded_file)
                else:
                    encoding = detect_encoding(uploaded_file)
                    text = uploaded_file.read().decode(encoding)
                with st.spinner(text="Generating Anki cards..."):
                    qa_pairs = generate_questions_from_text(text, num_questions, user_input, client, model, max_tokens, system)
        else:
            with st.spinner(text="Generating Anki cards..."):
                qa_pairs = generate_questions(num_questions, user_input, client, model, max_tokens, system)
    else:
        st.error("Please enter your Anthropic API key.")
    
    qa_pairs = qa_pairs.strip()
    st.success("Anki deck generated successfully!")
    st.download_button("Download the file", data=qa_pairs, file_name="question_answer_pairs.txt", mime="text/plain")