from sqlalchemy import (
    Column,
    String,
    Text
)

from .database import Base



class Task(Base):

    __tablename__="tasks"


    id=Column(
        String,
        primary_key=True
    )


    principal=Column(
        String,
        index=True
    )


    context_id=Column(
        String
    )


    batch_id=Column(
        String
    )


    state=Column(
        String
    )


    history=Column(
        Text
    )


    artifacts=Column(
        Text
    )



class Idempotency(Base):

    __tablename__="idempotency"


    key=Column(
        String,
        primary_key=True
    )


    body_hash=Column(
        String
    )


    task_id=Column(
        String
    )