from fastapi import APIRouter

router = APIRouter()

@router.get("/callback")
async def google_dev_auth_callback(code: str | None = None):
    return {"code": code}
