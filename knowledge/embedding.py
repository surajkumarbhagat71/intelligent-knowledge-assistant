from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    """
    Text ko embedding vector me convert karta hai.
    """

    embedding = model.encode(text)

    return embedding.tolist()


