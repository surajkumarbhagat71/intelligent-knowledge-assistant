from pgvector.django import CosineDistance
from .embedding import generate_embedding
from .models import DocumentChunk


def search_similar_chunks(query, top_k=3):
    """
    Search for chunks similar to the query using pgvector's CosineDistance.
    
    Args:
        query (str): The query text to search for
        top_k (int): Number of top results to return
        
    Returns:
        list: List of dicts with 'chunk' and 'score' keys
    """
    query_embedding = generate_embedding(query)

    results_queryset = (
        DocumentChunk.objects
        .annotate(
            distance=CosineDistance(
                "embedding",
                query_embedding
            )
        )
        .order_by("distance")[:top_k]
    )
    
    # Convert to list of dicts with 'chunk' and 'score' keys for compatibility with rag.py
    results = [
        {
            "chunk": chunk,
            "score": 1 - chunk.distance  # Convert distance to similarity score (1 - distance)
        }
        for chunk in results_queryset
    ]
    
    return results



def build_context(results):
    context_parts = []

    for result in results:
        chunk = result["chunk"]
        context_parts.append(
            f"Source: {chunk.document.title}\n"
            f"Page: {chunk.page_number}\n\n"
            f"{chunk.content}"
        )

    return "\n\n---\n\n".join(context_parts)






#---------------- this is manual code for more core concepts ------------

# import numpy as np

# from .models import DocumentChunk
# from .embedding import generate_embedding


# def cosine_similarity(vector_a, vector_b):
#     vector_a = np.array(vector_a)
#     vector_b = np.array(vector_b)

#     return np.dot(vector_a, vector_b) / (
#         np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
#     )


# def search_similar_chunks(query, top_k=3):
#     query_embedding = generate_embedding(query)

#     chunks = DocumentChunk.objects.all()

#     results = []

#     for chunk in chunks:
#         if not chunk.embedding:
#             continue

#         score = cosine_similarity(
#             query_embedding,
#             chunk.embedding
#         )

#         results.append({
#             "chunk": chunk,
#             "score": float(score),
#         })

#     results.sort(
#         key=lambda item: item["score"],
#         reverse=True
#     )

#     return results[:top_k]


# def build_context(results):
#     context_parts = []

#     for result in results:
#         chunk = result["chunk"]

#         context_parts.append(
#             f"Source: {chunk.document.title}\n"
#             f"Page: {chunk.page_number}\n\n"
#             f"{chunk.content}"
#         )

#     return "\n\n---\n\n".join(context_parts)