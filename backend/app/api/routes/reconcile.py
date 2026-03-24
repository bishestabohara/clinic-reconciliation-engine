from fastapi import APIRouter, Depends

from app.core.security import require_api_key
from app.schemas.reconcile import MedicationReconcileRequest, MedicationReconcileResponse
from app.services.reconciliation_service import reconcile_medications


router = APIRouter(prefix="/api/reconcile", tags=["reconcile"], dependencies=[Depends(require_api_key)])


@router.post("/medication", response_model=MedicationReconcileResponse)
def reconcile_medication(payload: MedicationReconcileRequest) -> MedicationReconcileResponse:
    return reconcile_medications(payload)
