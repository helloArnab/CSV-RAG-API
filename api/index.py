from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
from database import insert_file, insert_rows, get_files, get_rows_by_file_id, delete_file
from utils import parse_csv, process_csv, compute_similarity
from llm import generate_response
from models import FilePath, QueryRequest, UploadResponse, FilesResponse, QueryResponse, DeleteResponse
import pandas as pd
from mangum import Mangum

app = FastAPI()

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(None), file_path: FilePath = None):
    if file:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are accepted.")
        df = parse_csv(file.file)
        file_name = file.filename
    elif file_path:
        if not file_path.path.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are accepted.")
        try:
            df = parse_csv(file_path.path)
            file_name = file_path.path.split("/")[-1]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="No file or file path provided")

    file_id = str(uuid.uuid4())
    try:
        insert_file(file_id, file_name)
        rows = process_csv(df, file_id)
        insert_rows(rows)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {str(e)}")

    return UploadResponse(file_id=file_id, message="Upload successful")

@app.get("/files", response_model=FilesResponse)
async def list_files():
    try:
        files = get_files()
        files_list = [{"file_id": file["_id"], "file_name": file["file_name"]} for file in files]
        return FilesResponse(files=files_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_file(request: QueryRequest):
    file_id = request.file_id
    query = request.query
    if not query or not file_id:
        raise HTTPException(status_code=400, detail="Missing file_id or query")

    rows = get_rows_by_file_id(file_id)
    if not rows:
        raise HTTPException(status_code=404, detail="File not found or no data available")

    top_k_rows = compute_similarity(query, rows)
    context = " ".join([row["text"] for row in top_k_rows])
    response = generate_response(query, context)
    return QueryResponse(response=response)

@app.delete("/file/{file_id}", response_model=DeleteResponse)
async def delete_file_endpoint(file_id: str):
    try:
        if not delete_file(file_id):
            raise HTTPException(status_code=404, detail="File not found")
        return DeleteResponse(message="File deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

# Vercel serverless handler
handler = Mangum(app)