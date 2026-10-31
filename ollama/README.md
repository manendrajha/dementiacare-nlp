
# DementiaCare Companion – Ollama Model

DementiaCare Companion is a locally hosted conversational model configuration
built on top of Meta's Llama 3.2 3B model using Ollama.

It is configured for supportive, patient, dementia-aware everyday conversations.

## Base Model

- Model: llama3.2:3b
- Runtime: Ollama
- Deployment: Local inference
- Custom model name: dementiacare-companion

The custom configuration uses a Modelfile to define the system instructions
and generation parameters.

## Prerequisites

1. Install Ollama: https://ollama.com/
2. Ensure Ollama is running.
3. Have sufficient disk space and memory for the base model.

## Create the Model

Pull the base model:

```bash
ollama pull llama3.2:3b
```

Navigate to this directory:

```bash
cd ollama
```

Build the custom model:

```bash
ollama create dementiacare-companion -f Modelfile
```

## Run the Model

```bash
ollama run dementiacare-companion
```

## API Integration

The FastAPI backend communicates with Ollama through its local HTTP API.

Default endpoint:

```text
http://localhost:11434/api/chat
```

The backend uses the following configuration:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=dementiacare-companion
```

## Model Configuration

The Modelfile defines:

- Base model.
- Temperature.
- Context window.
- Repetition penalty.
- Dementia-aware conversational system instructions.

The system instructions emphasize:

- Short and clear responses.
- Patience with repeated questions.
- Emotional reassurance.
- Respectful communication.
- Avoiding invented personal memories.
- Avoiding medical diagnoses and medication advice.
- Redirecting urgent concerns to caregivers or professionals.

## Important Notes

- Model weights are not included in this repository.
- The base model is downloaded separately through Ollama.
- The custom model is created locally from the included Modelfile.
- Inference is performed locally; no paid model API is required by this configuration.
- Performance depends on the host machine's hardware.

## Limitations

This is an experimental conversational configuration for an academic project.
It is not a clinically validated medical system and must not replace professional
medical advice, diagnosis, treatment, or caregiver supervision.
