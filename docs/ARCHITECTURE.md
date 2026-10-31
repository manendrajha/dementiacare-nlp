
# DementiaCare – System Architecture

## 1. Overview

DementiaCare follows a client-server architecture.

The React frontend communicates with a FastAPI backend through HTTP APIs. The backend handles authentication, data access, NLP processing, memory retrieval, and communication with the locally hosted Ollama model.

MongoDB stores application data, including user information, memories, reminders, and conversation records.

## 2. Frontend Layer

The frontend is developed using React.

Responsibilities include:

- Patient-facing interface.
- Caregiver-facing interface.
- Authentication and account access.
- Displaying personal memories and reminders.
- Sending chat messages to the backend.
- Displaying conversational responses and history.

## 3. Backend Layer

The backend uses FastAPI and Python.

Responsibilities include:

- REST API endpoints.
- Authentication and authorization.
- Patient-caregiver access control.
- MongoDB communication.
- NLP classification and processing.
- Semantic memory retrieval.
- Ollama model integration.
- Conversation persistence.

## 4. NLP Processing

The NLP pipeline includes:

### Intent Classification

TF-IDF vectorization and Logistic Regression are used to classify incoming messages into supported conversational categories.

Examples include greetings, emotional support, family-related questions, memories, reminders, and activities.

### Emotion Classification

A separate TF-IDF and Logistic Regression pipeline estimates the emotional category of an incoming message.

### Semantic Memory Retrieval

Stored personal memories are searched for relevant information using semantic similarity.

This allows the application to retrieve relevant personal context when responding to memory-related questions.

## 5. Conversational Model

The application uses a locally hosted Llama 3.2 3B model through Ollama.

A custom Modelfile configures the model with:

- Dementia-aware communication instructions.
- Response generation parameters.
- Guidelines for handling repeated questions.
- Instructions to avoid fabricated personal information.
- Guidelines for avoiding unsupported medical advice.

The backend sends the conversation context and current user message to the Ollama API.

## 6. Conversation Flow

1. The user submits a message through the React interface.
2. The frontend sends the message to the FastAPI backend.
3. The backend authenticates the user and validates access.
4. The NLP pipeline classifies intent and emotion.
5. Depending on the intent, the backend retrieves relevant memories or reminders, or generates a conversational response using Ollama.
6. The response is returned to the frontend.
7. The conversation is stored in MongoDB.

## 7. Database Layer

MongoDB provides persistent storage for application data.

The backend uses asynchronous database operations.

Stored information includes application-specific user records, patient-caregiver relationships, memories, reminders, and conversation history.

## 8. Security Considerations

The application includes authentication and role-based access checks.

Sensitive configuration values are maintained through environment variables.

Further security hardening, privacy assessment, and deployment testing are required before real-world use.

## 9. Deployment Considerations

The current architecture supports local development.

The Ollama model must be available to the backend through its configured API endpoint.

A remote deployment would require appropriate model hosting, secure network communication, database access controls, and production-grade configuration.
