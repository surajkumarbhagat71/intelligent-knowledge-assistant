from django.shortcuts import render
from .rag import ask_rag


def chat(request):
    answer = None
    sources = []
    question = ""

    if request.method == "POST":
        question = request.POST.get("question", "").strip()

        if question:
            result = ask_rag(question)

            answer = result["answer"]
            sources = result["sources"]

    return render(
        request,
        "chart.html",
        {
            "question": question,
            "answer": answer,
            "sources": sources,
        },
    )
    
    
    

from django.shortcuts import render
from .agent.agent import run_agent


def agent_chat(request):
    answer = None
    tools = []
    sources = []

    if request.method == "POST":
        question = request.POST.get("question", "").strip()

        if question:
            result = run_agent(question)

            answer = result.get("answer", "")
            tools = result.get("tools", [])
            sources = result.get("sources", [])

    return render(
        request,
        "agent.html",
        {
            "answer": answer,
            "tools": tools,
            "sources": sources,
        },
    )