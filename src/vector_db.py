import faiss
import numpy as np

def build_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

def save_index(index, path="faiss_index.bin"):
    faiss.write_index(index, path)

def load_index(path="faiss_index.bin"):
    return faiss.read_index(path)

def search(index, query_vector, k=3):
    D, I = index.search(query_vector, k)
    return I