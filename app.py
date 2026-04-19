import pickle
from src.vector_db import load_index
from src.rag_pipeline import generate_answer

# Load index
index = load_index("faiss_index.bin")

# Load chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print("Constitution RAG Chatbot Ready")

while True:
    query = input("\nAsk question (or type exit): ")

    if query.lower() == "exit":
        break

    answer = generate_answer(query, index, chunks)
    print("\nAnswer:\n", answer)