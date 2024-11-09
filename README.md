
# legalSphere.API 🌐

This repository hosts the **FastAPI** backend for **LegalSphere**, an AI-based legal research engine designed to support in-depth case analysis and research. This backend is responsible for handling API requests, managing case data, and interfacing with the RAG model to deliver comprehensive case insights.

For the main LegalSphere repository, visit **[LegalSphere Web](https://github.com/sarfarajansari/legalSphere.Web)**.

## Project Overview

The **legalSphere.API** backend provides the essential APIs and services required to:
- Receive case information and queries from the frontend.
- Connect to LegalSphere’s advanced **Retrieval-Augmented Generation (RAG) model** to analyze cases.
- Retrieve insights on case strengths, weaknesses, evidence, and relevant past cases.
- Handle file (proof) image uploads and user authentication.

## Key Features

- **Case Analysis API**  
  A robust API that interacts with the RAG model, fetching comprehensive analysis results such as case strengths, weaknesses, supporting evidence, and similar past cases.

- **File Handling**  
  Manages uploads of image files and documentation needed as proof, ensuring secure storage and access.


## Tech Stack

- **FastAPI**: High-performance backend framework for building APIs.
- **Mongo DB**: Stores case data, user information, and proof documents.
- **Qdrant DB**: Stores past  cases as vectors for fast retrival and semantic search
- **Langchain**: RAG model for advanced analysis.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/sarfarajansari/legalSphere.API.git
   cd legalSphere.API
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables and configure database settings.

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

5. Visit `http://127.0.0.1:8000/docs` for API documentation.

## Related Repositories

- [legalSphere.Web](https://github.com/sarfarajansari/legalSphere.Web): The main web application repository for LegalSphere, which uses this API for its backend.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
