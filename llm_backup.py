# import numpy as np
# from src.embeddings import model
# from src.vector_db import search

# # =========================
# # 🔹 LLM PROVIDERS
# # =========================

# # Primary (current)
# from ollamafreeapi import OllamaFreeAPI
# ollama_client = OllamaFreeAPI()

# # --- OPTIONAL PROVIDERS (UNCOMMENT WHEN NEEDED) ---

# # 1. OpenAI (paid / fallback)
# # from openai import OpenAI
# # openai_client = OpenAI(api_key="YOUR_API_KEY")

# # 2. Groq (fast + cheap)
# # from groq import Groq
# # groq_client = Groq(api_key="YOUR_API_KEY")

# # 3. Together AI
# # from together import Together
# # together_client = Together(api_key="YOUR_API_KEY")

# # 4. HuggingFace Inference API
# # from huggingface_hub import InferenceClient
# # hf_client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.1")

# # =========================
# # 🔹 RETRIEVAL FUNCTION
# # =========================

# def retrieve(query, index, chunks, k=3):
#     query_vec = model.encode([query])
#     query_vec = np.array(query_vec).astype("float32")

#     indices = search(index, query_vec, k)
#     results = [chunks[i] for i in indices[0]]

#     return results

# # =========================
# # 🔹 LLM CALL HANDLER (SWITCH LOGIC)
# # =========================

# def call_llm(prompt):
#     """
#     Try multiple providers if one fails
#     """

#     # 🔹 1. Try Ollama (FREE)
#     try:
#         response = ollama_client.chat(
#             model="gpt-oss:20b",
#             prompt=prompt,
#             temperature=0.3
#         )
#         return response

#     except Exception as e:
#         print("Ollama failed:", e)

#     # 🔹 2. Try Groq (UNCOMMENT TO USE)
#     """
#     try:
#         response = groq_client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print("Groq failed:", e)
#     """

#     # 🔹 3. Try OpenAI (UNCOMMENT TO USE)
#     """
#     try:
#         response = openai_client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=800
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print("OpenAI failed:", e)
#     """

#     # 🔹 4. HuggingFace fallback
#     """
#     try:
#         response = hf_client.text_generation(prompt)
#         return response
#     except Exception as e:
#         print("HF failed:", e)
#     """

#     return "❌ All AI providers failed. Please try again later."

# # =========================
# # 🔹 MAIN GENERATION FUNCTION
# # =========================

# def generate_answer(query, index, chunks):
#     docs = retrieve(query, index, chunks)
#     context = "\n\n".join(docs)

#     prompt = f"""
# You are an expert in Indian Constitution.

# Rules:
# - Answer ONLY from context
# - If not found, say "Not found in document"
# - Explain simply and clearly
# - Do NOT cut sentences
# - Do NOT add random numbers
# - Use proper formatting (bullet points if needed)
# - Be concise but complete
# - If query is unrelated, say:
#   "I can only answer questions related to the Indian Constitution."

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     response = call_llm(prompt)

#     # 🔹 Post-processing (fix incomplete outputs)
#     if isinstance(response, str):
#         cleaned = response.strip()

#         # basic truncation fix
#         if len(cleaned) < 50 or cleaned.endswith(("1", "2", "3")):
#             cleaned += "\n\n(Please ask again if response seems incomplete.)"

#         return cleaned

#     return response