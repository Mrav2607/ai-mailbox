from pydantic import BaseModel

class ThreadRequest(BaseModel):
    thread_id: str

class TriageResponse(BaseModel):
    bucket: str
    items: list[dict]
