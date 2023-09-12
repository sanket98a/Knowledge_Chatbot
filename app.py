import streamlit as st
import os
import pdfplumber
from src.short2kb import ShortText
from src.neo4j import DataLoad


# Create a folder to store the uploaded files
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Function to save uploaded files
def save_uploaded_file(uploaded_file):
    with open(os.path.join('uploads', uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return st.sidebar.success("File saved successfully.")

# Function to read and display the content of a selected PDF file
def read_pdf(file_path):
    pdf_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text()
    return pdf_text



# Create a file upload widget
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "txt", "pdf"])

if uploaded_file is not None:
    # Display the file name
    st.sidebar.write("Uploaded file:", uploaded_file.name)

    # Save the uploaded file
    save_uploaded_file(uploaded_file)

# File selection dropdown
files = os.listdir('uploads')
selected_file = st.sidebar.selectbox("Select a file to view", files)

# Display the selected file's content
if selected_file.strip().endswith('.pdf'):
    st.write("Viewing file:", selected_file)
    txt_content = read_pdf(os.path.join('uploads', selected_file))
    st.text(txt_content)
elif selected_file.strip().endswith('.txt'):
    # Read and display the content of the .txt file
    with open(os.path.join('uploads', selected_file), "r") as file:
        txt_content=file.read()
    st.text(txt_content)
if txt_content:
    short_obj=ShortText()
    model,tokenizer=short_obj.model_tokenizer()
    kb=short_obj.from_small_text_to_kb(model,tokenizer,txt_content)
    kb.print()
    ## push the kb to graph Database(neo4j)
    data_obj=DataLoad()
    data_obj.load_data(kb)
    st.sidebar.success("Entity Relation data created sucessfully. Push to Databse.")












