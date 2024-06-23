import streamlit as st
#import anthropic
from PIL import Image
from openai import OpenAI
import io
import pytesseract

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    #"[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("Specimen Label OCR")

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
    if ocr_text.strip() and openai_api_key:
        try:
            client = OpenAI(api_key=openai_api_key)
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                # messages=[{"role": "system", "content": "You are a helpful assistant."}],
                prompt=f"Process all the text extracted from an image: {ocr_text}"
            )

            # Display the processed text
            st.write("Processed Text:")
            # st.text(response['choices'][0]['message']['content'].strip())
            st.text(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("No text was extracted from the image or OpenAI API key is missing.")


    # Use OpenAI GPT to process the extracted text
    # if ocr_text.strip():
        # Use OpenAI GPT to process the extracted text
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4", #this is a chat model, not suitable in this case
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": f"Process the following text extracted from an image: {ocr_text}"}
    #         ],
    #         max_tokens=500
    #     )

        # Display the processed text
    #     st.write("Processed Text:")
    #     st.text(response['choices'][0]['message']['content'].strip())
    # else:
    #     st.write("No text was extracted from the image.")
