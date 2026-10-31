
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.database.connection import database
from app.core.dependencies import require_role
from app.core.patient_access import get_accessible_patient_id

from app.nlp.intent_classifier import classify_intent
from app.nlp.emotion_classifier import classify_emotion
from app.nlp.semantic_memory import (
    find_relevant_memory as semantic_memory_search
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "dementiacare-companion"
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


def format_time(time_value):
    if not time_value:
        return "an unspecified time"

    try:
        return datetime.strptime(
            time_value, "%H:%M"
        ).strftime("%I:%M %p").lstrip("0")

    except (ValueError, TypeError):
        return str(time_value)


async def generate_conversational_response(
    message: str,
    patient_data_id: str
):
    """
    Generate a natural response using Ollama,
    including recent conversation history and
    current date/time context.
    """

    # CURRENT DATE AND TIME
    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    current_datetime = now.strftime(
        "%A, %d %B %Y, %I:%M %p"
    )

    system_context = f"""
You are the conversational companion of DementiaCare.

CURRENT DATE AND TIME:
{current_datetime}
Timezone: Asia/Kolkata (India).

Use this information when answering questions about today's
date, the day of the week, or the current time.

Never guess the current date or time.
Do not confuse the current date with dates mentioned in
previous conversations.

You provide friendly, respectful and supportive everyday
conversation for older adults, including people living with dementia.

COMMUNICATION:
- Speak naturally, warmly and professionally.
- Treat every person as an adult.
- Never use childish or patronising language.
- Never use terms like sweetie, dear or little one.
- Prefer short, clear sentences.
- Usually respond in 1 to 3 sentences.
- Ask no more than one question at a time.
- Avoid unnecessary lists and lengthy explanations.

DEMENTIA-AWARE INTERACTION:
- Acknowledge feelings before offering suggestions.
- Be patient with repeated questions and stories.
- Never shame someone for forgetting something.
- Avoid testing their memory.
- Offer gentle redirection when appropriate.
- Provide simple choices.
- Support dignity and independence.

EMOTIONAL SUPPORT:
- Recognise sadness, loneliness, anxiety and frustration.
- Respond with validation and reassurance.
- Never dismiss or minimise emotions.
- Do not make promises you cannot keep.

FACTUAL GROUNDING:
- Never invent personal memories, meals, appointments,
  family relationships or preferences.
- Never claim someone previously told you something
  unless it is explicitly present in the supplied context.
- If you do not know a personal fact, say so honestly.
- Distinguish suggestions from verified information.

SAFETY:
- Do not diagnose medical conditions.
- Do not recommend changing medication or treatment.
- For urgent concerns, encourage contacting a trusted
  caregiver or healthcare professional.
- Validate emotions without asserting uncertain facts.

CONVERSATION:
- Support ordinary everyday conversation.
- Discuss hobbies, weather and daily activities.
- Respond directly to what the person says.
- Never pretend to be human or a family member.

Your priority is to make the person feel heard,
respected, comfortable and safe.
"""

    # FETCH RECENT CONVERSATION HISTORY
    history = await database["conversations"].find(
        {"patient_id": patient_data_id},
        {
            "message": 1,
            "response": 1,
            "_id": 0
        }
    ).sort(
        "created_at", -1
    ).limit(6).to_list(length=6)

    history.reverse()

    # SYSTEM CONTEXT
    messages = [
        {
            "role": "system",
            "content": system_context
        }
    ]

    # PREVIOUS CONVERSATION
    for conversation in history:
        previous_message = conversation.get("message")
        previous_response = conversation.get("response")

        if previous_message:
            messages.append({
                "role": "user",
                "content": previous_message
            })

        if previous_response:
            messages.append({
                "role": "assistant",
                "content": previous_response
            })

    # CURRENT MESSAGE
    messages.append({
        "role": "user",
        "content": message
    })

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.65,
            "num_ctx": 4096,
            "repeat_penalty": 1.15
        }
    }

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60.0, connect=3.0)
    ) as client:

        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload
        )

        response.raise_for_status()

        result = response.json()

        return result.get(
            "message", {}
        ).get("content", "").strip()


@router.post("/")
async def chat(
    request: ChatRequest,
    current_user=Depends(require_role("patient")),
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    message = request.message.strip()

    # INTENT CLASSIFICATION
    classification = classify_intent(message)

    intent = classification["intent"]
    confidence = classification["confidence"]

    # EMOTION CLASSIFICATION
    emotion_result = classify_emotion(message)

    emotion = emotion_result["emotion"]
    emotion_confidence = emotion_result["confidence"]

    response = ""

    # FAMILY INFORMATION
    if intent == "family":

        memories = await database["memories"].find({
            "patient_id": patient_data_id,
            "category": "People"
        }).to_list(length=100)

        if memories:
            names = [
                memory.get("description", "")
                for memory in memories
                if memory.get("description")
            ]

            response = (
                "Your family is an important part of your life. "
                + " ".join(names[:2])
            )
        else:
            response = (
                "I don't have any family details saved yet. "
                "Would you like to tell me about someone special?"
            )

    # PERSONAL MEMORY RETRIEVAL
    elif intent == "memory":

        memories = await database["memories"].find({
            "patient_id": patient_data_id
        }).to_list(length=100)

        retrieval_result = semantic_memory_search(
            message,
            memories
        )

        print("SEMANTIC RETRIEVAL:", retrieval_result)

        if (
            isinstance(retrieval_result, dict)
            and "memory" in retrieval_result
        ):
            matched_memory = retrieval_result["memory"]

            description = (
                matched_memory.get("description", "")
                .strip()
                .rstrip(".!?")
            )

            response = (
                f"You shared that {description}. "
                "Would you like to talk about it?"
            )
        else:
            response = (
                "I don't have a specific memory about that yet. "
                "Your caregiver can add more details to your memory profile."
            )

    # REMINDER RETRIEVAL
    elif intent == "reminder":

        reminders = await database["reminders"].find({
            "patient_id": patient_data_id
        }).sort(
            "time", 1
        ).to_list(length=10)

        if reminders:
            reminder = reminders[0]

            response = (
                f"You have a reminder: "
                f"{reminder.get('title', 'Scheduled activity')} "
                f"at {format_time(reminder.get('time'))}."
            )
        else:
            response = (
                "You don't have any reminders scheduled right now."
            )

    # GENERAL CONVERSATION THROUGH OLLAMA
    else:

        try:
            response = await generate_conversational_response(
                message,
                patient_data_id
            )

            if not response:
                response = (
                    "I'm here with you. Would you like to tell me "
                    "a little more?"
                )

        except httpx.TimeoutException:
            print("Ollama request timed out.")

            response = (
                "I'm sorry, it is taking me a little longer to respond. "
                "Would you like to try again?"
            )

        except httpx.HTTPError as error:
            print("Ollama HTTP error:", error)

            response = (
                "I'm having a little trouble responding right now. "
                "We can try chatting again in a moment."
            )

        except Exception as error:
            print("Chat generation error:", error)

            response = (
                "I'm here with you. Would you like to tell me "
                "a little more?"
            )

    # SAVE CONVERSATION
    await database["conversations"].insert_one({
        "patient_id": patient_data_id,
        "message": message,
        "response": response,
        "intent": intent,
        "intent_confidence": confidence,
        "emotion": emotion,
        "emotion_confidence": emotion_confidence,
        "created_at": datetime.now(timezone.utc)
    })

    return {
        "message": message,
        "intent": intent,
        "confidence": confidence,
        "emotion": emotion,
        "emotion_confidence": emotion_confidence,
        "response": response
    }
