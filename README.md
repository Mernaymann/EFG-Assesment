# EFG HR Policy QA System

A simple question-answering system for HR policies. The system retrieves relevant policy sections and generates answers grounded in the provided HR documents.

This project was built as part of the **EFG Applied AI Data Scientist Technical Screener**.

## Project Overview

The system allows a user to ask natural-language questions about the provided HR policies and receive:

* A concise answer based on the policy documents
* The document and section used as the source
* A clear response when the policies do not contain the requested information

The project uses a local retrieval-augmented generation approach, so no external LLM API or API key is required.

## Design and Approach

### 1. Document Processing

The 10 Markdown policy documents are loaded and split into sections using their `##` headings.

For each section, the system keeps:

* Document ID
* Document title
* Section name
* Section content

Keeping this metadata makes it possible to show the source of each answer.

### 2. Embeddings

I used `sentence-transformers/all-MiniLM-L6-v2` to create embeddings for the policy sections and user questions.

I chose this model because it is lightweight, runs locally, and is suitable for semantic similarity search on a small document collection.

### 3. Retrieval

FAISS is used to search the policy embeddings and retrieve the most relevant sections.

A distance threshold is applied so that questions that are sufficiently different from the available policies can be treated as unanswerable instead of forcing the system to return an unrelated document.

### 4. Answer Generation

The retrieved policy content is passed to `google/flan-t5-small`.

The prompt instructs the model to:

* Use only the retrieved policy content
* Give a short and direct answer
* Avoid adding information not stated in the policy
* Prefer the general/default rule unless the question asks about a specific condition

### 5. Backend

The backend is implemented using FastAPI.

The main endpoint is:

```text
POST /ask
```

It accepts a natural-language question and returns the generated answer together with the relevant source information.

### 6. Frontend

The frontend is implemented using Streamlit.

It sends the user's question to the FastAPI backend and displays the answer and its source.

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

## Models

The project uses the following Hugging Face models:

* Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
* Answer generation: `google/flan-t5-small`

The models are downloaded automatically by the Python libraries on first run and are cached locally. Model weights are not included in this repository.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
```

On Windows:

```powershell
venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

The first run will download the required Hugging Face models automatically.

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

Handling questions outside the document set is an important part of the system.

If the similarity search does not find a sufficiently relevant policy section, the system returns:

```text
I couldn't find this information in the HR policies.
```

The system does not return an unrelated policy source for an unanswerable question.

An example is included in `sample_qa.md`.

## Source Attribution

For answerable questions, the API returns the most relevant policy document and section used for the answer.

This allows the user to verify the source of the response.

## Testing

The system was manually tested with:

* Answerable questions from different HR policies
* Questions requiring specific policy conditions
* An unanswerable question outside the provided policy set
* The FastAPI `/ask` endpoint
* The Streamlit frontend

Example test cases and their outputs are included in `sample_qa.md`.

## Known Limitations

* The current system uses a small local language model, so generated answers may be less capable than answers from larger models.
* Retrieval currently uses a simple FAISS similarity search with a fixed distance threshold.
* The answer generation step currently uses the most relevant retrieved policy section rather than combining multiple sections.
* The current implementation is designed for a small static document collection and does not include a persistent vector database.
* Model loading happens when the backend starts, so the first startup can take some time while models are loaded.
* The current frontend is intentionally simple and focuses on functionality rather than visual design.

## What I Would Improve With More Time

With more development time, I would:

* Evaluate retrieval quality systematically using a larger set of labelled questions.
* Compare different embedding models and tune the retrieval threshold based on validation results.
* Improve multi-section retrieval for questions that require information from more than one policy section.
* Add automated tests for the API, retrieval logic, and unanswerable-question handling.
* Add document-level and answer-level evaluation metrics.
* Improve the frontend with clearer source presentation and loading/error states.
* Add persistent indexing so embeddings do not need to be rebuilt every time the backend starts.

## AI Assistance

AI assistants were used during development for coding support, debugging, documentation, and development guidance.

The implementation was tested and validated during development, and the final project structure and behavior were reviewed before submission.

## Sample Questions

See `sample_qa.md` for 5 example questions, their answers, source documents, and an unanswerable question.
