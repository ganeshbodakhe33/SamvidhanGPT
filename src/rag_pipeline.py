import numpy as np
from src.embeddings import model
from src.vector_db import search
from ollamafreeapi import OllamaFreeAPI

client = OllamaFreeAPI()

def retrieve(query, index, chunks, k=3):
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    indices = search(index, query_vec, k)

    results = [chunks[i] for i in indices[0]]
    return results

def generate_answer(query, index, chunks):
    docs = retrieve(query, index, chunks)
    context = "\n\n".join(docs)

    prompt = f"""
You are an expert in Indian Constitution.

Rules:
- Welcome and greet the user only when necessary (like for first-time ask or based on need) and ask how you can help them.
- Answer ONLY from context
- If not found, say "Not found in document"
- Explain simply
- If the user query is is short, ask for more details to understand better
- Try to be concise and to the point
- Be polite and respectful
- Try to be as interesting as possible while answering, use examples and analogies to explain complex concepts
- Also do normal conversation, ask follow up questions, and be engaging and ask user to ask more questions about the constitution, and share interesting facts about it
- If the user query is not related to the constitution, politely say "I can only answer questions related to the Indian Constitution. Please ask something about it."

Context:
{context}

Question:
{query}
"""

    response = client.chat(
        model="gpt-oss:20b",
        prompt=prompt,
        temperature=0.3
    )

    return response