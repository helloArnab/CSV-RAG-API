# CSV RAG API

An API and UI for uploading and querying CSV files using Retrieval-Augmented Generation (RAG).

## Features
- Upload CSV files via file upload or file path.
- Store CSV data in MongoDB with embeddings.
- Query data using RAG with FLAN-T5.
- Interactive Streamlit UI for file management and chat.

## Prerequisites
- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- Git

## Setup Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/helloArnab/CSV-RAG-API.git
   cd csv_rag_api
   ```


## Install dependencies
    ```bash
    pip install -r requirements.txt
    ```


## Run the FastAPI app
    ```bash
    uvicorn app.main:app --reload
    ```


## Run the Streamlit App
    ```bash
    streamlit run streamlit_app.py
    ```