
from collections import Counter

from fastapi import APIRouter, Depends

from app.database.connection import database

from app.core.patient_access import get_accessible_patient_id


router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"]
)


FOLLOW_UP_KEYWORDS = {
    "sadness": [
        "sad", "lonely", "alone", "depressed", "unhappy",
        "miss", "cry", "upset"
    ],
    "fear": [
        "scared", "afraid", "worried", "anxious", "frightened"
    ],
    "distress": [
        "help", "pain", "hurt", "confused", "lost",
        "cannot", "can't", "difficult"
    ]
}


def generate_narrative_summary(records):
    messages = [
        record.get("message", "").strip()
        for record in records
        if record.get("message", "").strip()
    ]

    if not messages:
        return "No patient messages are available for analysis."

    intents = {
        record.get("intent", "unknown")
        for record in records
    }

    intent_descriptions = {
        "greeting": "greeted the assistant",
        "memory": "asked about previously shared personal memories",
        "emotional_support": "expressed a need for emotional support",
        "family": "discussed family-related topics",
        "activity": "expressed interest in activities",
        "orientation": "asked an orientation-related question",
        "reminder": "discussed reminders",
        "gratitude": "expressed gratitude",
        "goodbye": "ended a conversation"
    }

    observations = [
        description
        for intent, description in intent_descriptions.items()
        if intent in intents
    ]

    if observations:
        if len(observations) == 1:
            interaction_text = observations[0]
        else:
            interaction_text = (
                ", ".join(observations[:-1])
                + " and "
                + observations[-1]
            )

        summary = (
            f"Across the {len(messages)} recorded exchanges, "
            f"the patient {interaction_text}."
        )
    else:
        summary = (
            f"The patient participated in {len(messages)} "
            "recorded exchanges."
        )

    unknown_messages = [
        record.get("message", "").strip()
        for record in records
        if record.get("intent", "unknown") == "unknown"
        and record.get("message", "").strip()
    ]

    if unknown_messages:
        quoted_messages = [
            f'"{message}"'
            for message in unknown_messages[:3]
        ]

        if len(quoted_messages) == 1:
            message_text = quoted_messages[0]
        else:
            message_text = (
                ", ".join(quoted_messages[:-1])
                + " and "
                + quoted_messages[-1]
            )

        summary += (
            f" The patient also mentioned: {message_text}. "
            "These messages were not assigned a recognized intent."
        )

    return summary


def identify_follow_up_messages(records):
    follow_up = []

    for record in reversed(records):
        message = record.get("message", "").strip()
        message_lower = message.lower()

        matched_categories = []

        for category, keywords in FOLLOW_UP_KEYWORDS.items():
            if any(keyword in message_lower for keyword in keywords):
                matched_categories.append(category)

        if matched_categories:
            follow_up.append({
                "message": message,
                "categories": matched_categories,
                "created_at": (
                    record["created_at"].isoformat()
                    if record.get("created_at")
                    else None
                )
            })

    return follow_up[-5:]


@router.get("/")
async def get_conversations(
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    records = await database["conversations"].find({
        "patient_id": patient_data_id
    }).sort("created_at", -1).to_list(length=100)

    conversations = []

    for record in records:
        conversations.append({
            "id": str(record["_id"]),
            "message": record.get("message", ""),
            "response": record.get("response", ""),
            "intent": record.get("intent", "unknown"),
            "intent_confidence": record.get("intent_confidence", 0),
            "emotion": record.get("emotion", "unknown"),
            "emotion_confidence": record.get("emotion_confidence", 0),
            "created_at": (
                record["created_at"].isoformat()
                if record.get("created_at")
                else None
            )
        })

    return {
        "count": len(conversations),
        "conversations": conversations
    }


@router.get("/summary")
async def get_conversation_summary(
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    records = await database["conversations"].find({
        "patient_id": patient_data_id
    }).sort("created_at", -1).to_list(length=100)

    if not records:
        return {
            "total_exchanges": 0,
            "analysed_exchanges": 0,
            "summary": "No conversations have been recorded yet.",
            "emotion_observations": "",
            "common_intents": [],
            "detected_emotions": [],
            "key_messages": [],
            "follow_up_messages": []
        }

    recent_records = records[:20]

    intent_counts = Counter(
        record.get("intent", "unknown")
        for record in recent_records
    )

    emotion_counts = Counter(
        record.get("emotion", "unknown")
        for record in recent_records
        if record.get("emotion") not in (
            None, "neutral", "unknown"
        )
    )

    common_intents = [
        {"intent": intent, "count": count}
        for intent, count in intent_counts.most_common(5)
    ]

    detected_emotions = [
        {"emotion": emotion, "count": count}
        for emotion, count in emotion_counts.most_common(5)
    ]

    key_messages = [
        record.get("message", "")
        for record in reversed(recent_records[:5])
        if record.get("message")
    ]

    narrative_summary = generate_narrative_summary(
        recent_records
    )

    emotion_description = (
        ", ".join(
            f"{item['emotion']} ({item['count']})"
            for item in detected_emotions
        )
        if detected_emotions
        else "No non-neutral emotions were detected."
    )

    follow_up_messages = identify_follow_up_messages(
        recent_records
    )

    return {
        "total_exchanges": len(records),
        "analysed_exchanges": len(recent_records),
        "summary": narrative_summary,
        "emotion_observations": emotion_description,
        "common_intents": common_intents,
        "detected_emotions": detected_emotions,
        "key_messages": key_messages,
        "follow_up_messages": follow_up_messages
    }
