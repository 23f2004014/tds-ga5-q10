from fastapi import HTTPException

from .models import Idempotency
from .utils import hash_message



def check_request(
    db,
    principal,
    message
):


    key = (
        principal
        +
        ":"
        +
        message["messageId"]
    )


    digest = hash_message(
        message
    )


    record = db.query(
        Idempotency
    ).filter(
        Idempotency.key==key
    ).first()



    if record:


        if record.body_hash != digest:

            raise HTTPException(

                status_code=409,

                detail={
                    "code":
                    "IDEMPOTENCY_CONFLICT"
                }

            )


        return record.task_id



    return None





def save_request(
    db,
    principal,
    message,
    task_id
):


    key = (
        principal
        +
        ":"
        +
        message["messageId"]
    )


    record = Idempotency(

        key=key,


        body_hash=
        hash_message(message),


        task_id=task_id

    )


    db.add(record)

    db.commit()