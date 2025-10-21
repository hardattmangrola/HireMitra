import fitz 
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please create a .env file with your Groq API key.")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(uploaded_file):
    '''
    Extracts text from a PDF file.
    Accepts Streamlit UploadedFile, file-like objects, bytes, or a filesystem path.
    Returns the concatenated text of all pages.
    '''
    text = ""
    try:
        # Handle Streamlit's UploadedFile (has .read and .getvalue)
        if hasattr(uploaded_file, "getvalue"):
            pdf_bytes = uploaded_file.getvalue()
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        # Handle generic file-like object (e.g., BytesIO)
        elif hasattr(uploaded_file, "read") and not isinstance(uploaded_file, (str, bytes, bytearray)):
            pdf_bytes = uploaded_file.read()
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        # Handle raw bytes
        elif isinstance(uploaded_file, (bytes, bytearray)):
            with fitz.open(stream=uploaded_file, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        # Handle filesystem path (str)
        else:
            with open(uploaded_file, "rb") as f:
                pdf_bytes = f.read()
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
    except Exception as e:
        print(f"Error Reading {uploaded_file}: {e}")
    return text

def ask_groq(prompt,max_tokens=500):
    '''
    Asks a question to the Groq API and returns the response.
    Args:
    prompt (str): The question to ask the Groq API.
    max_tokens (int): The maximum number of tokens to return.
    Returns:
    str: The response from the Groq API.
    '''
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.5
    )
    return response.choices[0].message.content
