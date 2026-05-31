# Approach and Reflection

## Approach

* Built a PDF Question Answering application using FastAPI.
* Implemented PDF upload functionality to process user documents.
* Extracted text from uploaded PDFs.
* Split extracted text into smaller chunks for efficient retrieval.
* Generated embeddings for text chunks.
* Stored embeddings in a FAISS vector index.
* Used semantic search to retrieve relevant chunks based on user questions.
* Integrated Ollama to generate answers using the retrieved context.
* Added logging to store user questions and generated answers in a JSON file.
* Created an n8n workflow to automate weekly activity summaries.
* Configured the workflow to read logs, generate a summary, and send it through email.

## Challenges Faced

* Understanding the complete RAG pipeline and how each component connects together.
* Configuring Ollama and running local LLM inference.
* Integrating FAISS retrieval with answer generation.
* Managing file paths and permissions while working with n8n.
* Setting up Gmail SMTP and email automation.
* Debugging frontend issues related to file upload and page refresh behavior.
* Ensuring the backend APIs worked reliably before focusing on UI improvements.

## What I Would Improve

* Build a more polished frontend interface.
* Add support for multiple PDFs instead of a single active document.
* Store embeddings in a persistent vector database.
* Add user authentication and document management.
* Deploy the application for public access.
* Improve logging and monitoring features.
