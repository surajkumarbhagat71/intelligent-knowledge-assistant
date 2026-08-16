from langchain_openai import ChatOpenAI
from django.conf import settings

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from .tools import (
    search_knowledge_base,
    get_employee_leave,
    get_today_news,
    web_search,
    get_weather,
)


llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=settings.NVIDIA_API_KEY,
    model="openai/gpt-oss-20b",
    temperature=0.2,
)

tools = [
    search_knowledge_base,
    get_employee_leave,
    get_today_news,
    web_search,
    get_weather,
]

llm_with_tools = llm.bind_tools(tools)

tool_map = {
    "search_knowledge_base": search_knowledge_base,
    "get_employee_leave": get_employee_leave,
    "get_today_news": get_today_news,
    "web_search": web_search,
    "get_weather": get_weather,
}



def run_agent(question):

    messages = [
        SystemMessage(
            content=(
                "You are a helpful company AI assistant. "
                "Use the available tools whenever necessary. "
                "You can use multiple tools if the question requires "
                "information from different sources. "
                "Do not make up information."
            )
        ),
        HumanMessage(content=question),
    ]

    used_tools = []
    sources = []

    response = llm_with_tools.invoke(messages)

    while response.tool_calls:

        messages.append(response)

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_function = tool_map[tool_name]

            tool_result = tool_function(**tool_args)

            used_tools.append(tool_name)

            if isinstance(tool_result, dict):
                sources.extend(tool_result.get("sources", []))

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                )
            )

        response = llm_with_tools.invoke(messages)

    return {
        "answer": response.content,
        "tools": used_tools,
        "sources": sources,
    }









#single tool call ke liye ye function use kiya ja sakta hai.

# def run_agent(question):

#     messages = [
#         SystemMessage(
#             content=(
#                 "You are a helpful company AI assistant. "
#                 "Use the available tools when you need information "
#                 "from company documents. "
#                 "Do not make up information."
#             )
#         ),
#         HumanMessage(content=question),
#     ]

#     response = llm_with_tools.invoke(messages)

#     if response.tool_calls:

#         tool_call = response.tool_calls[0]

#         tool_name = tool_call["name"]
#         tool_args = tool_call["args"]

#         tool_function = tool_map[tool_name]

#         tool_result = tool_function(**tool_args)

#         messages.append(response)

#         messages.append(
#             ToolMessage(
#                 content=str(tool_result),
#                 tool_call_id=tool_call["id"],
#             )
#         )

#         final_response = llm.invoke(messages)

#         return {
#             "answer": final_response.content,
#             "tool": tool_name,
#             "sources":tool_result.get("sources", []),
#         }

#     return {
#         "answer": response.content,
#         "tool": None,
#         "sources":  tool_result.get("sources", []),
#     }