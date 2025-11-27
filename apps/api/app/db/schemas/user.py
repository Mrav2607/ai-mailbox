from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    email: str
    display_name: str | None = None
