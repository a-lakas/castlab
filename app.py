# app.py

import os
import streamlit as st
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from detectron2.config import get_cfg
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import base64


data = base64.b64decode("c2staUE2cG5aWE1Pc3ZxUGc0TXZZdVhUM0JsYmtGSnRrTHEzUHVGcUVvZVZlY2lLTENy")
decoded_data = data.decode('utf-8')

api_key = decoded_data
# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = api_key

# Set up Detectron2
cfg = get_cfg()
cfg.MODEL.DEVICE = 'cpu'  # GPU is recommended

# Download PDF file
pdf_url = "https://s21.q4cdn.com/399680738/files/doc_financials/2022/q4/Meta-12.31.2022-Exhibit-99.1-FINAL.pdf"
response = requests.get(pdf_url)
pdf_path = 'docs/Meta-12.31.2022-Exhibit-99.1-FINAL.pdf'

with open(pdf_path, 'wb') as pdf_file:
    pdf_file.write(response.content)

# Load PDF document
text_folder = 'docs'
loaders = [UnstructuredPDFLoader(os.path.join(text_folder, fn)) for fn in os.listdir(text_folder)]
index = VectorstoreIndexCreator().from_loaders(loaders)

# Streamlit UI
st.title("ChatPDF Streamlit App")

# OCR Function
def perform_ocr(image):
    text = pytesseract.image_to_string(image)
    return text

# File Upload
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Perform OCR"):
        if uploaded_file.type == "application/pdf":
            # PDF OCR
            st.write("Performing OCR on PDF...")
            pdf_text = ''
            pdf_images = index.extract_images_from_pdf(pdf_path)
            for pdf_image in pdf_images:
                image = Image.open(BytesIO(pdf_image))
                pdf_text += perform_ocr(image)
            st.write(pdf_text)
        else:
            # Image OCR
            st.write("Performing OCR on Image...")
            image = Image.open(uploaded_file)
            image_text = perform_ocr(image)
            st.write(image_text)
