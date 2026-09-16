\# EFG HR Policy QA System



A simple question-answering system for HR policies. The system retrieves relevant policy sections and generates grounded answers based only on the provided HR documents.



\## Project Overview



This project was developed as part of the EFG Applied AI Data Scientist technical assessment.



The system allows users to ask natural-language questions about company HR policies and receive:



\- A concise answer based on the HR policy documents

\- The relevant policy document and section

\- A clear response when the requested information cannot be found



\## Architecture



The system consists of:



1\. \*\*Document Processing\*\*

&#x20;  - Loads the 10 HR policy Markdown files

&#x20;  - Splits documents into sections using `##` headings

&#x20;  - Preserves document title, filename, and section information for source attribution



2\. \*\*Embeddings\*\*

&#x20;  - Uses `all-MiniLM-L6-v2` from Sentence Transformers

&#x20;  - Converts policy sections and user questions into vector embeddings



3\. \*\*Retrieval\*\*

&#x20;  - Uses FAISS for similarity search

&#x20;  - Retrieves the most relevant policy sections

&#x20;  - Applies a similarity threshold to handle questions that are not covered by the policies



4\. \*\*Answer Generation\*\*

&#x20;  - Uses the local `google/flan-t5-small` model

&#x20;  - Generates answers using the retrieved policy content only



5\. \*\*Backend\*\*

&#x20;  - Built with FastAPI

&#x20;  - Provides a `/ask` endpoint for questions



6\. \*\*Frontend\*\*

&#x20;  - Built with Streamlit

&#x20;  - Provides a simple interface for asking questions and viewing answers and sources



\## Project Structure



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

└── sample\_qa.md

Requirements

Python 3.10+

FastAPI

Uvicorn

Streamlit

Sentence Transformers

FAISS

Transformers

PyTorch



The application uses local models and does not require an OpenAI API key.



Installation



Create and activate a virtual environment:



python -m venv venv



Windows:



venv\\Scripts\\activate



Install dependencies:



pip install -r requirements.txt

Running the Backend



Open a terminal and navigate to the backend directory:



cd backend

python -m uvicorn main:app --reload



The API will be available at:



http://127.0.0.1:8000



Interactive API documentation:



http://127.0.0.1:8000/docs

Running the Frontend



Open another terminal from the project root and run:



cd frontend

python -m streamlit run app.py



The Streamlit application will open in the browser.



Example API Request

{

&#x20; "question": "How many annual leave days do employees get?"

}



Example response:



{

&#x20; "question": "How many annual leave days do employees get?",

&#x20; "answer": "Employees are entitled to 21 working days of annual leave.",

&#x20; "sources": \[

&#x20;   {

&#x20;     "document": "Annual Leave Policy",

&#x20;     "section": "Entitlement",

&#x20;     "document\_id": "01-annual-leave.md"

&#x20;   }

&#x20; ]

}

Handling Unanswerable Questions



If a question is not covered by the HR policy documents, the system returns:



I couldn't find this information in the HR policies.



No unrelated policy source is returned for an unanswerable question.



Source Attribution



Each answerable response includes the most relevant source document and section used to answer the question.



This helps users verify where the answer came from and keeps the generated response grounded in the provided HR policies.



Sample Questions



See sample\_qa.md for example questions and expected answers, including an unanswerable question.



AI Assistance



AI-assisted development was used during the implementation of this project for coding support, debugging, documentation, and development guidance.



The final implementation, testing, and validation were reviewed and performed as part of the project development process.

