from pydantic import BaseModel

class FilePath(BaseModel):
    path: str

class QueryRequest(BaseModel):
    file_id: str
    query: str

class UploadResponse(BaseModel):
    file_id: str
    message: str

class FilesResponse(BaseModel):
    files: list[dict]

class QueryResponse(BaseModel):
    response: str

class DeleteResponse(BaseModel):
    message: str