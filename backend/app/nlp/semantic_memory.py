
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the pretrained sentence embedding model.
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def find_relevant_memory(message, memories, threshold=0.50):
    """
    Retrieve the most semantically relevant personal memory.

    Returns:
        {
            "memory": matched memory document,
            "similarity": similarity score
        }

        Returns None if no sufficiently relevant memory exists.
    """

    if not memories:
        return None

    memory_texts = []

    for memory in memories:
        title = memory.get("title", "")
        description = memory.get("description", "")
        category = memory.get("category", "")

        combined_text = (
            f"{title}. {description}. Category: {category}"
        )

        memory_texts.append(combined_text)

    query_embedding = embedding_model.encode(
        [message],
        normalize_embeddings=True
    )

    memory_embeddings = embedding_model.encode(
        memory_texts,
        normalize_embeddings=True
    )

    similarities = cosine_similarity(
        query_embedding,
        memory_embeddings
    )[0]

    best_index = int(similarities.argmax())
    best_score = float(similarities[best_index])

    if best_score < threshold:
        return None

    return {
        "memory": memories[best_index],
        "similarity": round(best_score, 4)
    }
