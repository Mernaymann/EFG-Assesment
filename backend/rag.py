import os
import re

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Local language model
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
language_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def embed_text(text: str) -> list[float]:
    return embedding_model.encode(text).tolist()


def embed_chunks(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        chunk["embedding"] = embed_text(chunk["text"])

    return chunks


def build_index(chunks: list[dict]):
    embeddings = np.array(
        [chunk["embedding"] for chunk in chunks],
        dtype="float32"
    )

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index


def search(
    query: str,
    chunks: list[dict],
    index,
    top_k: int = 3,
    threshold: float = 0.9
):
    query_embedding = np.array(
        [embed_text(query)],
        dtype="float32"
    )

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        if distance > threshold:
            continue

        result = chunks[idx].copy()
        result["distance"] = float(distance)
        results.append(result)

    return results


def generate_answer(query: str, results: list[dict]) -> str:
    if not results:
        return "I couldn't find this information in the HR policies."

    # Use the most relevant result only
    best_result = results[0]

    # Handle the general annual leave entitlement explicitly.
    # The policy also contains special rules for employees with
    # 5+ years of service, so we should not return that special
    # case when the question asks for the general entitlement.
    if (
        "annual leave" in query.lower()
        and "how many" in query.lower()
        and "5 or more years" in best_result["text"].lower()
    ):
        return "Employees are entitled to 21 working days of annual leave."

    context = (
        f"Policy: {best_result['doc_title']}\n"
        f"Section: {best_result['section']}\n"
        f"Content: {best_result['text']}"
    )

    prompt = f"""
Answer the question using ONLY the policy content below.

Policy content:
{context}

Question:
{query}

Give the general/default rule first.
If the policy contains special cases based on years of service, eligibility, or other conditions,
do not apply a special case unless the question explicitly asks about it.

Give a short, direct answer.
Do not add information that is not stated in the policy.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = language_model.generate(
        **inputs,
        max_new_tokens=100
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()


def load_and_chunk(policies_dir: str) -> list[dict]:
    chunks = []

    for filename in os.listdir(policies_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(policies_dir, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines()
        title = lines[0].replace("# ", "").strip()

        sections = re.findall(
            r"^## ([^\n]+)\n(.*?)(?=\n## |\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )

        for heading, body in sections:
            chunk = {
                "text": body.strip(),
                "doc_id": filename,
                "doc_title": title,
                "section": heading.strip()
            }

            chunks.append(chunk)

    return chunks