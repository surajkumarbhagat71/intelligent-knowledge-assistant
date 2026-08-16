from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from django.conf import settings
from langchain_core.output_parsers import StrOutputParser

from .retrieval import search_similar_chunks, build_context


RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the user's question using only the provided context.

If the answer is not available in the context, say:
"I could not find the answer in the provided document."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""
)


llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=settings.NVIDIA_API_KEY,
    model="openai/gpt-oss-20b",
    temperature=0.2,
)


rag_chain = RAG_PROMPT | llm | StrOutputParser()


def ask_rag(question):
    results = search_similar_chunks(question, top_k=3)

    context = build_context(results)

    answer  = rag_chain.invoke({
        "context": context,
        "question": question,
    })

    return {
        "answer": answer,
        "sources": [
            {
                "document": result["chunk"].document.title,
                "page": result["chunk"].page_number,
                "score": result["score"],
            }
            for result in results
        ],
    }










# from langchain_core.prompts import ChatPromptTemplate


# RAG_PROMPT = ChatPromptTemplate.from_template(
#     """
# You are a helpful AI assistant.

# Answer the user's question using only the provided context.

# If the answer is not available in the context, say:
# "I could not find the answer in the provided document."

# Do not make up information.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
# )


# from langchain_openai import ChatOpenAI
# from django.conf import settings

# from .retrieval import search_similar_chunks, build_context



# def ask_rag(question):
#     results = search_similar_chunks(question,top_k=3)

#     context = build_context(results)

#     prompt = RAG_PROMPT.format(
#         context=context,
#         question=question,
#     )
    
#     llm = ChatOpenAI(
#         base_url="https://integrate.api.nvidia.com/v1",
#         api_key=settings.NVIDIA_API_KEY,
#         model="openai/gpt-oss-20b",
#         temperature=0.2,
#     )

#     response = llm.invoke(prompt)

#     return {
#         "answer": response.content,
#         "sources": [
#             {
#                 "document": result["chunk"].document.title,
#                 "page": result["chunk"].page_number,
#                 "score": result["score"],
#             }
#             for result in results
#         ],
#     }
    
    
