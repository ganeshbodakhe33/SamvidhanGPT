from src.loader import load_pdf
from src.chunker import chunk_text
from src.embeddings import get_embeddings
from src.vector_db import build_index, save_index
import numpy as np
import pickle

# Step 1: Load PDF
text = load_pdf("data/constitution.pdf")

# Step 2: Chunk
chunks = chunk_text(text)

# Step 3: Embeddings
embeddings = get_embeddings(chunks)
embeddings = np.array(embeddings)

# Step 4: Build index
index = build_index(embeddings)

# Save index
save_index(index)

# Save chunks
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Index built and saved")