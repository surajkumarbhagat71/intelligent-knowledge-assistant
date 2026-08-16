"""
===========================================================
        INTERNAL COMPANY KNOWLEDGE ASSISTANT
                 PROJECT DIAGRAM / NOTES
===========================================================

This file is only for learning, revision and architecture
reference.

No actual application logic should be written here.
"""


# ==========================================================
# 1. COMPLETE PROJECT OVERVIEW
# ==========================================================

"""
                    USER
                      |
                      v
                DJANGO UI
                      |
                      v
                 AI AGENT
                      |
              +-------+-------+
              |               |
              v               v
        RAG TOOL         EMPLOYEE TOOL
              |               |
              v               v
        COMPANY PDF       DJANGO DATABASE
              |               |
              v               v
         DOCUMENTS        EMPLOYEE DATA
              |               |
              +-------+-------+
                      |
                      v
                     LLM
                      |
                      v
                FINAL ANSWER


WHY?
----
We are building an internal company AI assistant that can
answer questions from company documents as well as
company database information.

The Agent decides which tool is required for the question.
"""


# ==========================================================
# 2. RAG - RETRIEVAL AUGMENTED GENERATION
# ==========================================================

"""
RAG means:

Retrieval + Augmented + Generation


USER QUESTION
     |
     v
Question Embedding
     |
     v
Similarity Search
     |
     v
Relevant Document Chunks
     |
     v
Build Context
     |
     v
LLM
     |
     v
FINAL ANSWER


WHY RAG?
--------
LLM does not automatically know our private company documents.

Instead of sending the complete PDF to the LLM every time,
we retrieve only the relevant information and provide it
to the LLM as context.
"""


# ==========================================================
# 3. PDF DOCUMENT PROCESSING
# ==========================================================

"""
PDF
 |
 v
PdfReader
 |
 v
Extract Text
 |
 v
DocumentChunk
 |
 v
Database


Example:

Company Leave Policy.pdf

Page 1
   |
   +-- Chunk 0
   +-- Chunk 1
   +-- Chunk 2

Page 2
   |
   +-- Chunk 3
   +-- Chunk 4


WHY CHUNKS?
-----------
Large documents should not be searched or sent to the LLM
as one huge block.

Smaller chunks make semantic search more useful and allow
us to retrieve only relevant information.
"""


# ==========================================================
# 4. DocumentChunk MODEL
# ==========================================================

"""
DocumentChunk stores individual pieces of a document.

Fields:

document
content
chunk_index
page_number
created_at


Example:

document = Company Leave Policy 2026
page_number = 1
chunk_index = 0

content =
"Full-time employees are entitled to 18 days
of annual leave..."


WHY page_number?
----------------
We want to show the user where the answer came from.

Example:

Source:
Company Leave Policy 2026
Page: 1
"""


# ==========================================================
# 5. EMBEDDING
# ==========================================================

"""
TEXT
 |
 v
Sentence Transformer
 |
 v
VECTOR

Example:

"Python is a high level programming language."

        |
        v

[0.12, -0.04, 0.31, ...]


Our embedding model produces:

384 dimensions


WHY EMBEDDINGS?
---------------
Computers cannot directly understand the semantic meaning
of sentences like humans.

Embeddings convert text into numerical vectors so that
semantically similar text can be compared.
"""


# ==========================================================
# 6. EMBEDDING MODEL VS LLM
# ==========================================================

"""
IMPORTANT:

Embedding Model
----------------
Sentence Transformer

Purpose:
Convert text into vectors.

        TEXT
         |
         v
    EMBEDDING MODEL
         |
         v
      VECTOR


LLM
---
NVIDIA / GPT OSS model

Purpose:
Understand context and generate natural language answers.

        CONTEXT
           |
           v
          LLM
           |
           v
       ANSWER


They have different responsibilities.
"""


# ==========================================================
# 7. VECTOR / SIMILARITY SEARCH
# ==========================================================

"""
USER QUESTION

"How many annual leaves does an employee get?"
             |
             v
      Question Embedding
             |
             v
       Similarity Search
             |
             v

Chunk 0 -> Score: 0.4547
Chunk 1 -> Score: 0.4045
Chunk 4 -> Score: 0.3558

             |
             v

Top relevant chunks
"""


# ==========================================================
# 8. search_knowledge_base()
# ==========================================================

"""
search_knowledge_base()

This is our RAG TOOL.

Flow:

Question
   |
   v
Embedding
   |
   v
Similarity Search
   |
   v
Relevant Chunks
   |
   v
Build Context
   |
   v
LLM
   |
   v
Answer + Sources


Example:

Question:
"How many annual leaves does an employee get?"

Answer:
"Full-time employees are entitled to 18 days
of annual leave."


Sources:
Company Leave Policy 2026
Page 1
"""


# ==========================================================
# 9. build_context()
# ==========================================================

"""
Retrieved chunks are converted into a readable context
for the LLM.

Example:

Source: Company Leave Policy 2026
Page: 1

Full-time employees are entitled to 18 days
of annual leave.

---

Source: Company Leave Policy 2026
Page: 2

...


WHY?
----
The database returns chunks as objects/results.

The LLM needs a clean text context to understand the
retrieved information.
"""


# ==========================================================
# 10. RAG VS AGENT
# ==========================================================

"""
RAG
---

RAG mainly answers questions from documents.

Example:

User:
"How many annual leaves are allowed?"

        |
        v
RAG
        |
        v
Company Policy PDF
        |
        v
Answer


AGENT
-----

Agent can decide which tool to use.

Example:

User:
"How many leaves does Rahul have?"

        |
        v
Agent
        |
        v
Employee Tool
        |
        v
Database
        |
        v
Answer


MAIN DIFFERENCE:

RAG:
Retrieve information from documents.

Agent:
Decide what action/tool is required.
"""


# ==========================================================
# 11. EMPLOYEE DATABASE
# ==========================================================

"""
Employee
    |
    | OneToOne
    v
LeaveBalance


Employee:

employee_code
name
email
department
designation
joining_date


LeaveBalance:

employee
year
total_leaves
used_leaves
remaining_leaves


Example:

Rahul Kumar

Total Leaves: 18
Used Leaves: 4
Remaining: 14
"""


# ==========================================================
# 12. get_employee_leave()
# ==========================================================

"""
get_employee_leave()

This is our second Agent tool.

Flow:

Employee Name
     |
     v
Django ORM
     |
     v
Employee
     |
     v
LeaveBalance
     |
     v
Result


Example:

get_employee_leave("Rahul Kumar")


Result:

{
    "found": True,
    "employee_name": "Rahul Kumar",
    "total_leaves": 18,
    "used_leaves": 4,
    "remaining_leaves": 14
}


WHY?
----
Employee leave information is stored in our database,
not inside the company PDF.

Therefore RAG cannot provide this information.

The Agent uses the database tool.
"""


# ==========================================================
# 13. AI AGENT
# ==========================================================

"""
                    USER
                      |
                      v
                    AGENT
                      |
             +--------+--------+
             |                 |
             v                 v
 search_knowledge_base   get_employee_leave
             |                 |
             v                 v
         PDF / RAG          Database
             |                 |
             +--------+--------+
                      |
                      v
                     LLM
                      |
                      v
                FINAL ANSWER


WHY AGENT?
----------
Because our application has multiple information sources
and multiple capabilities.

The Agent decides which tool is required.
"""


# ==========================================================
# 14. MULTI-TOOL AGENT
# ==========================================================

"""
The Agent can use more than one tool.

Example question:

"According to the company policy, how many annual leaves
are allowed and how many leaves does Rahul Kumar have
remaining?"


Agent
 |
 +----> search_knowledge_base()
 |             |
 |             v
 |       Annual Leave = 18
 |
 +----> get_employee_leave()
               |
               v
        Rahul Remaining = 14


Then:

Both results
     |
     v
    LLM
     |
     v
Final Answer:

"Employees are entitled to 18 annual leaves.
Rahul Kumar has 14 leaves remaining."


This is MULTI-TOOL AGENT behavior.
"""


# ==========================================================
# 15. TOOL CALLING
# ==========================================================

"""
LLM does not directly execute Python functions.

Instead:

LLM
 |
 | Tool Call
 v
Python Tool
 |
 v
Tool Result
 |
 v
LLM
 |
 v
Final Answer


Example:

LLM says:

get_employee_leave(
    employee_name="Rahul Kumar"
)


Python executes the function.

Result:

14 remaining leaves.


Then the result is sent back to the LLM.
"""


# ==========================================================
# 16. WHY ToolMessage?
# ==========================================================

"""
ToolMessage sends the result of a tool back to the LLM.

Flow:

LLM
 |
 v
Tool Call
 |
 v
Python Function
 |
 v
Tool Result
 |
 v
ToolMessage
 |
 v
LLM
 |
 v
Final Answer


Without returning the tool result to the LLM,
the LLM cannot use the information to generate
the final answer.
"""


# ==========================================================
# 17. OLD SINGLE TOOL AGENT
# ==========================================================

"""
OLD VERSION:

response.tool_calls[0]

Meaning:

Only the first tool call was processed.

We kept the old code commented for learning/reference.

It is NOT the current Agent implementation.
"""


# ==========================================================
# 18. CURRENT MULTI-TOOL AGENT
# ==========================================================

"""
CURRENT VERSION:

for tool_call in response.tool_calls:
    ...


This allows multiple tool calls.

Also:

while response.tool_calls:
    ...


This allows the Agent to perform multiple rounds of
tool calling when necessary.

Flow:

Question
   |
   v
LLM
   |
Tool Call?
   |
   +---- NO ----> Final Answer
   |
   YES
   |
   v
Execute Tool(s)
   |
   v
Send Results to LLM
   |
   v
LLM again
   |
   v
Tool Call?
   |
   ...
   |
   v
Final Answer
"""


# ==========================================================
# 19. TOOLS AND TOOL MAP
# ==========================================================

"""
Available tools:

tools = [
    search_knowledge_base,
    get_employee_leave,
]


tool_map:

{
    "search_knowledge_base": search_knowledge_base,
    "get_employee_leave": get_employee_leave
}


WHY tool_map?
-------------
The LLM returns a tool name.

Python needs to find the actual function associated
with that name.
"""


# ==========================================================
# 20. DJANGO AGENT UI
# ==========================================================

"""
We created a SEPARATE UI for the Agent.

RAG UI
------
Existing RAG interface remains separate.


AGENT UI
--------
/knowledge/agent/


Flow:

Browser
   |
   v
Django Template
   |
   v
agent_chat()
   |
   v
run_agent()
   |
   v
AI Agent
   |
   v
Tools
   |
   v
LLM
   |
   v
Answer
   |
   v
Template
"""


# ==========================================================
# 21. CURRENT PROJECT STATUS
# ==========================================================

"""
COMPLETED:

[✓] Django Project
[✓] KnowledgeDocument
[✓] PDF Upload
[✓] PDF Text Extraction
[✓] DocumentChunk
[✓] Page Number Tracking
[✓] Embeddings
[✓] Sentence Transformer
[✓] Similarity Search
[✓] RAG
[✓] Context Building
[✓] NVIDIA LLM
[✓] RAG Tool
[✓] Employee Model
[✓] LeaveBalance Model
[✓] Employee Leave Tool
[✓] AI Agent
[✓] Tool Calling
[✓] Multi-Tool Agent
[✓] Agent Django UI


CURRENT TOOLS:

1. search_knowledge_base
2. get_employee_leave
"""


# ==========================================================
# 22. COMPLETE END-TO-END FLOW
# ==========================================================

"""
                    USER
                      |
                      v
                DJANGO TEMPLATE
                      |
                      v
                  run_agent()
                      |
                      v
                 AI AGENT / LLM
                      |
             +--------+--------+
             |                 |
             v                 v
       RAG TOOL          EMPLOYEE TOOL
             |                 |
             v                 v
        PDF CHUNKS        DJANGO DATABASE
             |                 |
             v                 v
        VECTOR SEARCH      LEAVE BALANCE
             |                 |
             +--------+--------+
                      |
                      v
                     LLM
                      |
                      v
                FINAL ANSWER
                      |
                      v
                DJANGO TEMPLATE
                      |
                      v
                    USER
"""


# ==========================================================
# 23. SIMPLE INTERVIEW EXPLANATION
# ==========================================================

"""
RAG:

"I extract text from company PDF documents and store the
content as document chunks. I generate embeddings for
the chunks using a Sentence Transformer model. When a user
asks a question, I generate an embedding for the question,
retrieve the most similar chunks, and provide them as
context to the LLM. The LLM generates the final answer
with document sources."


AI AGENT:

"On top of the RAG system, I built an AI Agent with multiple
tools. The Agent decides which tool to use based on the
user's question. One tool searches company documents using
RAG, while another retrieves employee leave information
from the Django database."


MULTI-TOOL:

"For questions requiring information from multiple sources,
the Agent can call multiple tools and then provide the
combined information to the LLM to generate the final answer."
"""


# ==========================================================
# 24. MOST IMPORTANT THING TO REMEMBER
# ==========================================================

"""
RAG = FIND RELEVANT INFORMATION

LLM = UNDERSTAND + GENERATE ANSWER

TOOL = PERFORM A SPECIFIC TASK

AGENT = DECIDE WHICH TOOL(S) TO USE

DATABASE = STORE STRUCTURED COMPANY DATA

DOCUMENT = STORE UNSTRUCTURED COMPANY KNOWLEDGE

EMBEDDING = CONVERT TEXT INTO NUMERICAL VECTOR

VECTOR SEARCH = FIND SEMANTICALLY SIMILAR CONTENT

MULTI-TOOL AGENT = USE MULTIPLE TOOLS WHEN REQUIRED
"""


# ==========================================================
# END
# ==========================================================