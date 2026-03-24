from fastapi import APIRouter, Depends

from app.core.security import require_api_key
from app.schemas.quality import DataQualityRequest, DataQualityResponse
from app.services.quality_service import validate_data_quality


router = APIRouter(
    prefix="/api/validate",
    tags=["quality"],
    dependencies=[Depends(require_api_key)],
)


@router.post("/data-quality", response_model=DataQualityResponse)
def validate_quality(payload: DataQualityRequest) -> DataQualityResponse:
    return validate_data_quality(payload)
