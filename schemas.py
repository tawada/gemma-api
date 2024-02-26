from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Body(BaseModel):
    messages: list[Message]


class Response(BaseModel):
    content: str
