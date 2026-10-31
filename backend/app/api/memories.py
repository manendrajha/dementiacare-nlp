
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database.connection import database
from app.schemas.memory import MemoryCreate, MemoryUpdate
from app.utils import serialize_document, validate_object_id
from app.core.patient_access import get_accessible_patient_id


router = APIRouter(
    prefix="/api/memories",
    tags=["Memories"]
)

memory_collection = database["memories"]


@router.post("/")
async def create_memory(
    memory: MemoryCreate,
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    now = datetime.now(timezone.utc)

    document = memory.model_dump()
    document["patient_id"] = patient_data_id
    document["created_at"] = now
    document["updated_at"] = now

    result = await memory_collection.insert_one(document)

    saved = await memory_collection.find_one({
        "_id": result.inserted_id,
        "patient_id": patient_data_id
    })

    return serialize_document(saved)


@router.get("/")
async def get_memories(
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    cursor = memory_collection.find({
        "patient_id": patient_data_id
    }).sort("created_at", -1)

    memories = []

    async for document in cursor:
        memories.append(serialize_document(document))

    return memories


@router.put("/{memory_id}")
async def update_memory(
    memory_id: str,
    memory: MemoryUpdate,
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    object_id = validate_object_id(memory_id)

    result = await memory_collection.update_one(
        {
            "_id": object_id,
            "patient_id": patient_data_id
        },
        {
            "$set": {
                **memory.model_dump(),
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    updated = await memory_collection.find_one({
        "_id": object_id,
        "patient_id": patient_data_id
    })

    return serialize_document(updated)


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: str,
    patient_data_id: str = Depends(get_accessible_patient_id)
):
    object_id = validate_object_id(memory_id)

    result = await memory_collection.delete_one({
        "_id": object_id,
        "patient_id": patient_data_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return {"message": "Memory deleted successfully"}
