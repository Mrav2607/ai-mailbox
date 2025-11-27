from pydantic import BaseModel

class Mail(BaseModel):
    to: str
    subject: str
    body: str
