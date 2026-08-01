import json
import uuid

from .models import Task



def create_task(
    db,
    principal,
    batch,
    proposals
):


    task = Task(

        id=str(uuid.uuid4()),


        principal=principal,


        context_id=str(uuid.uuid4()),


        batch_id=batch["batchId"],


        state=
        "TASK_STATE_INPUT_REQUIRED",


        history=json.dumps(
            [
                batch
            ]
        ),


        artifacts=json.dumps(
            {
                "proposals":
                proposals
            }
        )

    )


    db.add(task)

    db.commit()

    db.refresh(task)


    return task