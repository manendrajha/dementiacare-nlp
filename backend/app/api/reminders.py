
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database.connection import database
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.utils import serialize_document, validate_object_id
from app.core.patient_access import get_accessible_patient_id


router = APIRouter(
    prefix="/api/reminders",
    tags=["Reminders"]
)

reminder_collection = database["reminders"]


@router.post("/")
async def create_reminder(
    reminder: ReminderCreate,
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    now = datetime.now(timezone.utc)

    document = reminder.model_dump()
    document["patient_id"] = patient_data_id
    document["created_at"] = now
    document["updated_at"] = now

    result = await reminder_collection.insert_one(document)

    saved = await reminder_collection.find_one({
        "_id": result.inserted_id,
        "patient_id": patient_data_id
    })

    return serialize_document(saved)


@router.get("/")
async def get_reminders(
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    cursor = reminder_collection.find({
        "patient_id": patient_data_id
    }).sort("time", 1)

    reminders = []

    async for document in cursor:
        reminders.append(serialize_document(document))

    return reminders


@router.put("/{reminder_id}")
async def update_reminder(
    reminder_id: str,
    reminder: ReminderUpdate,
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    object_id = validate_object_id(reminder_id)

    result = await reminder_collection.update_one(
        {
            "_id": object_id,
            "patient_id": patient_data_id
        },
        {
            "$set": {
                **reminder.model_dump(),
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    updated = await reminder_collection.find_one({
        "_id": object_id,
        "patient_id": patient_data_id
    })

    return serialize_document(updated)


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: str,
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    object_id = validate_object_id(reminder_id)

    result = await reminder_collection.delete_one({
        "_id": object_id,
        "patient_id": patient_data_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    return {"message": "Reminder deleted successfully"}
