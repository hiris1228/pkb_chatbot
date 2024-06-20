import streamlit as st
import anthropic
from PIL import Image
import openai
import io
import pytesseract

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
    #"[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("Specimen Label OCR with OpenAI GPT")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to text using Tesseract OCR
    ocr_text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    st.write("Extracted Text:")
    st.text(ocr_text)

    # Use OpenAI GPT to process the extracted text
    '''
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Process the following text extracted from an image: {ocr_text}",
        max_tokens=500
    )

    # Display the processed text
    st.write("Processed Text:")
    st.text(response.choices[0].text.strip())
    '''
    if ocr_text.strip():
        # Use OpenAI GPT to process the extracted text
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Process the following text extracted from an image: {ocr_text}"}
            ],
            max_tokens=500
        )

        # Display the processed text
        st.write("Processed Text:")
        st.text(response['choices'][0]['message']['content'].strip())
    else:
        st.write("No text was extracted from the image.")

