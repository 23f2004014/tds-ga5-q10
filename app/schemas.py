from pydantic import BaseModel
from typing import Any


class Message(BaseModel):

    messageId:str
    role:str
    parts:list


class A2AMessage(BaseModel):

    message:Message
    configuration:dict|None=None