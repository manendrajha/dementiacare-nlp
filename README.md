
# DementiaCare

An AI-assisted conversational support application designed to provide people living with dementia with accessible, patient, and supportive everyday interactions, while enabling caregivers to stay connected.

## Overview

DementiaCare is an academic NLP and full-stack application that explores how natural language processing and locally hosted language models can support everyday communication for people living with dementia.

The application combines traditional NLP techniques, database-backed personal memory, and a locally hosted Large Language Model to provide context-aware conversational assistance.

It also includes patient and caregiver functionality for managing relevant information and maintaining a connection between the two.

## Key Features

### AI Conversational Assistant
- Natural language conversations powered by a locally hosted Llama 3.2 3B model through Ollama.
- Custom system instructions designed for dementia-aware communication.
- Short, clear, supportive responses.
- Conversation history for contextual continuity.
- Current date and time awareness.

### NLP Components
- Intent classification using TF-IDF and Logistic Regression.
- Emotion classification using a TF-IDF and Logistic Regression pipeline.
- Semantic retrieval of stored personal memories.
- Intent-based routing between database-backed responses and LLM-generated conversations.

### Personal Memory
- Stores relevant personal information.
- Retrieves matching memories using semantic similarity.
- Supports responses grounded in available stored information.
- Avoids intentionally inventing personal facts when information is unavailable.

### Patient and Caregiver Functionality
- User authentication and role-based access.
- Patient-caregiver account linking.
- Patient and caregiver dashboards.
- Memory management.
- Reminder management.
- Conversation history.

## System Architecture

```text
                  React Frontend
                       |
                       | HTTP Requests
                       |
                  FastAPI Backend
                       |
          +------------+-------------+
          |            |             |
      Authentication  NLP        MongoDB
          |         Pipeline         |
          |            |             |
          |      +-----+------+      |
          |      |     |      |      |
          |   Intent Emotion Memory  |
          |   Model  Model Retrieval |
          |      |     |      |      |
          |      +-----+------+      |
          |            |             |
          |       Ollama API         |
          |            |             |
          |   DementiaCare Companion |
          |      (Llama 3.2 3B)      |
          +--------------------------+
```

### Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | MongoDB |
| Database Driver | PyMongo Async |
| NLP | Scikit-learn, TF-IDF, Logistic Regression |
| Semantic Retrieval | Embedding-based memory retrieval |
| LLM | Llama 3.2 3B |
| Local Model Runtime | Ollama |
| API Communication | HTTPX |
| Authentication | JWT |

## Project Structure

```text
dementia-bot-nlp/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── nlp/
│   │   └── schemas/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
│
├── ollama/
│   ├── Modelfile
│   └── README.md
│
├── docs/
│   └── ARCHITECTURE.md
│
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

The structure above is representative. Refer to the actual repository for the complete implementation.

## Getting Started

### Prerequisites

Install the following:

- Python 3.11 or a compatible Python version.
- Node.js and npm.
- MongoDB Community Server or a compatible MongoDB deployment.
- Ollama.

Useful links:

- Python: https://www.python.org/
- Node.js: https://nodejs.org/
- MongoDB: https://www.mongodb.com/try/download/community
- Ollama: https://ollama.com/

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/dementia-bot-nlp.git

cd dementia-bot-nlp
```

### 2. Configure Environment Variables

Create a `.env` file using the provided example:

```bash
cp .env.example .env
```

Update the values according to your local MongoDB configuration and application settings.

Never commit your actual `.env` file.

### 3. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend should be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Configure the Ollama Model

Install and start Ollama.

Pull the base model:

```bash
ollama pull llama3.2:3b
```

Navigate to the Ollama configuration directory from the project root:

```bash
cd ollama
```

Create the custom model:

```bash
ollama create dementiacare-companion -f Modelfile
```

Verify that the model is available:

```bash
ollama list
```

The backend uses:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=dementiacare-companion
```

For additional instructions, see [Ollama Setup](ollama/README.md).

### 5. Set Up the Frontend

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Use the local URL printed by Vite or your frontend development server.

## Running the Application

The following services should be running:

1. MongoDB database.
2. Ollama runtime with the custom DementiaCare model available.
3. FastAPI backend.
4. React frontend.

Start each service in its respective terminal.

## Configuration

Important environment variables:

| Variable | Purpose |
|---|---|
| MONGODB_URL | MongoDB connection string |
| DATABASE_NAME | Database name |
| SECRET_KEY | JWT signing secret |
| OLLAMA_URL | Local Ollama API address |
| OLLAMA_MODEL | Custom Ollama model name |

Refer to `.env.example` for the configuration template. Actual variable names must match the backend implementation.

## Design Considerations

DementiaCare explores several principles for accessible AI-assisted communication:

- Patience with repeated questions.
- Simple and understandable language.
- Emotional acknowledgement and reassurance.
- Retrieval of stored personal information when relevant.
- Respect for patient autonomy and dignity.
- Avoidance of unsupported medical claims.

## Limitations and Future Scope

This project is an academic prototype and has not been clinically validated.

Potential limitations include:

- NLP classification errors.
- Inaccurate or incomplete LLM responses.
- Dependence on stored memory quality.
- Local inference performance limitations.
- Need for further privacy, security, and accessibility testing.

Future improvements could include:

- More comprehensive evaluation of conversational quality.
- Improved semantic memory retrieval.
- Multilingual conversational support.
- Speech-based interaction.
- Expanded caregiver monitoring and accessibility features.
- Evaluation with appropriate domain experts and ethical oversight.

## Responsible Use

DementiaCare is intended as an experimental supportive communication tool.

It is not a medical device and does not provide diagnosis, treatment, or emergency assistance. It should not replace professional healthcare services or caregiver supervision.

Avoid entering sensitive personal or medical information into an untrusted deployment. Secure authentication, database access, and network communication before any real-world deployment.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- Meta AI for the Llama model family.
- Ollama for local model execution.
- The open-source Python and JavaScript ecosystems.
- The developers and researchers contributing to NLP and accessible computing.
