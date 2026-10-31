
from bson import ObjectId
from fastapi import HTTPException


DEMO_PATIENT_ID = "demo-patient-001"


def serialize_document(document):
    if not document:
        return None

    return {
        "id": str(document["_id"]),
        **{
            key: value
            for key, value in document.items()
            if key != "_id"
        }
    }


def validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid record ID"
        )

    return ObjectId(id)
