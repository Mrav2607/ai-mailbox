from pydantic import BaseModel

class DraftRequest(BaseModel):
    to: str
    subject: str
    body: str
