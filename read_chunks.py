import requests
import os
import json
import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    
    # 1. Catch server crashes or timeouts
    if r.status_code != 200:
        print(f"Server Error {r.status_code}: {r.text}")
        return []
        
    data = r.json()
    
    # 2. Catch internal Ollama errors
    if 'error' in data:
        print(f"Ollama Error: {data['error']}")
        return []
        
    # 3. Safely extract the embeddings list
    return data.get("embeddings", [])


jsons = os.listdir("jsons")  # List all the jsons 
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f"jsons/{json_file}") as f:
        content = json.load(f)
    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])
       
    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1

        my_dicts.append(chunk) 
        
    break
       
# print(my_dicts)

df = pd.DataFrame.from_records(my_dicts)

joblib.dump(df, "embeddings.joblib")
# print(df)



