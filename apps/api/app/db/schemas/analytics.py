from pydantic import BaseModel

class Overview(BaseModel):
    threads: int
    messages: int
    classified: int
