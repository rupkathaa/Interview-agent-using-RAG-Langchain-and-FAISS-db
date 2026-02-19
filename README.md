This project is a retrieval-augmented generation (RAG) system designed to act as a technical interview assistant. It uses a local large language model via Ollama to generate specific, role-based interview questions by referencing a provided knowledge base of PDF documents.


Project Structure:

create_memory.py: Handles data ingestion. It loads PDF files from a directory, splits the text into manageable chunks, generates vector embeddings, and saves them locally using FAISS.

app.py: The main application interface. It loads the saved vector store, initializes the LLM, and manages the conversational loop between the user and the agent.

prompt.py: Contains the custom prompt template and strict behavioral rules for the AI agent.

data/: Directory intended for storing source PDF documents (the knowledge base).

vectorstore/: Directory where the FAISS index is stored after processing.


Tech Stack:

Orchestration: LangChain

Vector Database: FAISS

LLM: Mistral (via Ollama)

Embeddings: nomic-embed-text (via Ollama)

Document Loading: PyPDF




How it Works:

Knowledge Base Creation: The system reads PDF files from the data/ folder. It uses RecursiveCharacterTextSplitter to break text into 500-character chunks with a 50-character overlap to maintain context.
Vector Storage: These chunks are converted into numerical embeddings using the nomic-embed-text model and stored in a FAISS index for fast similarity searching.
Interview Logic: When a user inputs a job description, the system searches the FAISS index for the most relevant technical information.
Constrained Response: The agent is governed by a strict prompt template that forces it to stay in character, evaluate answers as "Correct" or "Incorrect," and refuse non-interview related queries.
