import streamlit as st
import anthropic
from PIL import Image
import openai
import io

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
    #"[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Anthropic")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.")

if uploaded_file and question and anthropic_api_key:
    article = uploaded_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # "claude-2" for Claude 2 model
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)

st.title("Specimen Label OCR with OpenAI GPT")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    # Prepare the image for OCR processing
    # Convert the image to text using OpenAI API (GPT-4 model)
    response = openai.Image.create(
        file=img_bytes,
        purpose="document_ocr"
    )

    # Extract text from response
    text = response['choices'][0]['text']
    
    # Display the extracted text
    st.write("Extracted Text:")
    st.text(text)
