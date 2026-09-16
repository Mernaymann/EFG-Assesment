# EFG HR Policy QA System

A simple question-answering system for HR policies. It retrieves relevant policy sections and generates answers based only on the provided HR documents.

## Project Overview

This project was developed as part of the EFG Applied AI Data Scientist technical assessment.

The system allows users to ask natural-language questions about the company's HR policies and receive:

* A concise answer based on the HR policy documents
* The relevant policy document and section
* A clear response when the information cannot be found in the policies

## Architecture

The system has the following components:

### 1. Document Processing

* Loads the 10 HR policy Markdown files
* Splits each document into sections using `##` headings
* Keeps the document title, filename, and section for source attribution

### 2. Embeddings

* Uses `all-MiniLM-L6-v2` from Sentence Transformers
* Converts policy sections and user questions into vector embeddings

### 3. Retrieval

* Uses FAISS for similarity search
* Retrieves the most relevant policy sections
* Uses a similarity threshold to identify questions that are not covered by the policies

### 4. Answer Generation

* Uses the local `google/flan-t5-small` model
* Generates answers using the retrieved policy content

### 5. Backend

* Built with FastAPI
* Provides a `/ask` endpoint for questions

### 6. Frontend

* Built with Streamlit
* Provides a simple interface for asking questions and viewing answers and sources

## Project Structure

```text
EFG-Assesment/
├── backend/
│   ├── main.py
│   └── rag.py
├── frontend/
│   └── app.py
├── data/
│   └── policies/
│       ├── 01-annual-leave.md
│       ├── 02-sick-leave.md
│       ├── 03-remote-work.md
│       ├── 04-work-hours-overtime.md
│       ├── 05-expense-claims.md
│       ├── 06-business-travel.md
│       ├── 07-code-of-conduct.md
│       ├── 08-grievance-procedure.md
│       ├── 09-learning-development.md
│       └── 10-performance-reviews.md
├── .gitignore
├── requirements.txt
├── README.md
└── sample_qa.md
```

## Requirements

* Python 3.10+
* FastAPI
* Uvicorn
* Streamlit
* Sentence Transformers
* FAISS
* Transformers
* PyTorch

The application uses local models and does not require an OpenAI API key.

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```powershell
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Backend

Open a terminal and navigate to the `backend` directory:

```powershell
cd backend
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Frontend

Open another terminal and navigate to the `frontend` directory:

```powershell
cd frontend
python -m streamlit run app.py
```

The Streamlit application will open in the browser.

## Example API Request

```json
{
  "question": "How many annual leave days do employees get?"
}
```

Example response:

```json
{
  "question": "How many annual leave days do employees get?",
  "answer": "Employees are entitled to 21 working days of annual leave.",
  "sources": [
    {
      "document": "Annual Leave Policy",
      "section": "Entitlement",
      "document_id": "01-annual-leave.md"
    }
  ]
}
```

## Handling Unanswerable Questions

If a question is not covered by the HR policy documents, the system returns:

```text
I couldn't find this information in the HR policies.
```

No unrelated policy source is returned for an unanswerable question.

## Source Attribution

Each answerable response includes the most relevant source document and section used to answer the question.

This allows users to verify where the answer came from and keeps the generated response grounded in the provided HR policies.

## Sample Questions

See `sample_qa.md` for example questions and expected answers, including an unanswerable question.

## AI Assistance

AI-assisted development was used during the implementation of this project for coding support, debugging, documentation, and development guidance.

The final implementation, testing, and validation were reviewed and performed as part of the project development process.
