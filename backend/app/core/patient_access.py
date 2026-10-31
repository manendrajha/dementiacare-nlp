
from bson import ObjectId
from fastapi import Depends, HTTPException, Query

from app.database.connection import database
from app.core.dependencies import get_current_user


async def get_accessible_patient_id(
    patient_id: str | None = Query(
        default=None,
        description="Patient account ID. Required for caregivers."
    ),
    current_user=Depends(get_current_user)
):
    """
    Resolve the patient data ID accessible to the authenticated user.

    Patients access their own records.
    Caregivers must provide the account ID of a linked patient.
    """

    user_id = str(current_user["_id"])
    role = current_user.get("role")

    if role == "patient":
        if patient_id and patient_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Patients can only access their own records"
            )

        return current_user.get("legacy_patient_id", user_id)

    if role == "caregiver":
        if not patient_id or not ObjectId.is_valid(patient_id):
            raise HTTPException(
                status_code=400,
                detail="A valid patient account ID is required"
            )

        relationship = await database[
            "caregiver_relationships"
        ].find_one({
            "patient_user_id": patient_id,
            "caregiver_user_id": user_id
        })

        if not relationship:
            raise HTTPException(
                status_code=403,
                detail="You are not linked to this patient"
            )

        return relationship["patient_data_id"]

    raise HTTPException(
        status_code=403,
        detail="This account cannot access patient records"
    )
