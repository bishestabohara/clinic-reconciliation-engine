from typing import Optional

from fastapi import Header, HTTPException, status

from app.core.config import get_api_key

API_KEY_HEADER = "x-api-key"


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    expected_api_key = get_api_key()

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
