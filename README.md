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
   


## Install dependencies
    pip install -r requirements.txt
    


## Run the FastAPI app
    uvicorn app.main:app --reload
    


## Run the Streamlit App
    streamlit run streamlit_app.py


# Project Overview
![ss3](https://github.com/user-attachments/assets/bd6b9f56-d3ab-47ff-b413-ce328874ca94)
![ss1](https://github.com/user-attachments/assets/6de27639-7447-47ef-aae9-27692c048e62)




# Impotant NOTE (Bugs and issues)
1. I have tried to deploy the project on Render but it's not deploying due to memory issue in free deployment

![ss2](https://github.com/user-attachments/assets/166454b3-1783-4e73-8dbd-1338e1cc3326)

2. There is a bug on unloading and csv that api upload for infinite types

## I have build this project in one night due to shortage of time and ongoing college exams I will try to fix this once I get time
