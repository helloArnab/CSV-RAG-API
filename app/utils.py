import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def parse_csv(file):
    return pd.read_csv(file)

def generate_text(row):
    return ", ".join([f"{col}: {row[col]}" for col in row.index])

def process_csv(df: pd.DataFrame, file_id: str, batch_size=32):
    rows = []
    texts = df.apply(generate_text, axis=1).tolist()
    print(f"Generating embeddings for {len(texts)} rows in batches of {batch_size}")
    
    # Batch processing for embeddings
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_embeddings = embedder.encode(batch_texts, show_progress_bar=False)
        for j, (text, embedding) in enumerate(zip(batch_texts, batch_embeddings)):
            row_data = df.iloc[i + j].to_dict()
            rows.append({
                "file_id": file_id,
                "row_id": i + j,
                "text": text,
                "embedding": embedding.tolist(),
                "row_data": row_data
            })
        print(f"Processed batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")
    return rows

def compute_similarity(query: str, rows: list):
    query_embedding = embedder.encode(query)
    similarities = [np.dot(query_embedding, row["embedding"]) for row in rows]
    top_k_indices = np.argsort(similarities)[-5:][::-1]
    return [rows[i] for i in top_k_indices]

