import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("CSV RAG Chat")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    response = requests.post(f"{API_URL}/upload", files={"file": uploaded_file})
    if response.status_code == 200:
        st.success("File uploaded successfully")
        st.rerun()
    else:
        st.error(f"Error uploading file: {response.json()['detail']}")

# List files
response = requests.get(f"{API_URL}/files")
if response.status_code == 200:
    files = response.json()["files"]
    if files:
        selected_file = st.selectbox("Select a file", [file["file_name"] for file in files])
        selected_file_id = next(file["file_id"] for file in files if file["file_name"] == selected_file)
    else:
        st.write("No files uploaded yet.")
        selected_file_id = None
else:
    st.error("Error retrieving files")
    selected_file_id = None

# Chat interface
if selected_file_id:
    st.write("Chat with the selected CSV file:")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the CSV"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = requests.post(f"{API_URL}/query", json={"file_id": selected_file_id, "query": prompt})
        if response.status_code == 200:
            answer = response.json()["response"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            st.error(f"Error querying the API: {response.json()['detail']}")