import json
import threading
import os

from fastapi import (
    FastAPI,
    Depends,
    Header,
    HTTPException
)

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from .database import (
    Base,
    engine,
    get_db
)

from .models import Task

from .auth import authenticate

from .agent_card import create_card

from .decision import decide_invoice

from .storage import create_task

from .idempotency import (
    check_request,
    save_request
)

from .lifecycle import execute_results


Base.metadata.create_all(
    bind=engine
)


app = FastAPI()


BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000/a2a"
)


lock = threading.Lock()


def a2a_response(data):

    return JSONResponse(
        content=data,
        media_type="application/a2a+json"
    )



def check_headers(
    a2a_version: str | None = Header(None),
    content_type: str | None = Header(None)
):

    if a2a_version != "1.0":

        raise HTTPException(
            status_code=400,
            detail="Invalid A2A Version"
        )


    if content_type != "application/a2a+json":

        raise HTTPException(
            status_code=415,
            detail="Invalid media type"
        )



@app.get(
    "/.well-known/agent-card.json"
)
def card():

    return JSONResponse(
        content=create_card(BASE_URL),
        media_type="application/json"
    )



@app.post(
    "/a2a/message",
    dependencies=[
        Depends(check_headers)
    ]
)
def message(
    body: dict,
    user=Depends(authenticate),
    db: Session = Depends(get_db)

):

    msg = body["message"]


    old = check_request(
        db,
        user,
        msg
    )


    if old:

        task = db.get(
            Task,
            old
        )

        return a2a_response({
            "task": build_task(task)
        })


    data = msg["parts"][0]["data"]


    proposals = []


    for package in data["packages"]:

        proposals.append(
            decide_invoice(package)
        )


    task = create_task(
        db,
        user,
        data,
        proposals
    )


    save_request(
        db,
        user,
        msg,
        task.id
    )


    return a2a_response({
        "task": build_task(task)
    })



@app.post(
    "/a2a/tasks/{task_id}",
    dependencies=[
        Depends(check_headers)
    ]
)
def continue_task(
    task_id: str,
    body: dict,
    user=Depends(authenticate),
    db: Session = Depends(get_db)

):

    task = db.get(
        Task,
        task_id
    )


    if not task or task.principal != user:

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )



    with lock:


        if task.state == "TASK_STATE_COMPLETED":

            return a2a_response({
                "task": build_task(task)
            })


        data = body["message"]["parts"][0]["data"]


        receipt = execute_results(
            task,
            data
        )


        task.state = "TASK_STATE_COMPLETED"


        task.artifacts = json.dumps(
            receipt
        )


        db.commit()



    return a2a_response({
        "task": build_task(task)
    })



@app.get(
    "/a2a/tasks/{task_id}"
)
def get_task(
    task_id: str,
    user=Depends(authenticate),
    db: Session = Depends(get_db)

):

    task = db.get(
        Task,
        task_id
    )


    if not task or task.principal != user:

        raise HTTPException(
            status_code=404,
            detail="Not found"
        )


    return a2a_response({
        "task": build_task(task)
    })



@app.get(
    "/a2a/tasks"
)
def tasks(
    user=Depends(authenticate),
    db: Session = Depends(get_db)
):

    result = db.query(
        Task
    ).filter(
        Task.principal == user
    ).all()


    return a2a_response({

        "tasks": [
            build_task(t)
            for t in result
        ]

    })



def build_task(task):

    return {

        "id": task.id,

        "contextId": task.context_id,


        "status": {

            "state": task.state

        },


        "history": json.loads(
            task.history
        ),


        "artifacts": [

            {

                "parts": [

                    {

                        "mediaType":
                        "application/vnd.ga5.invoice-action-proposals+json",


                        "data":
                        json.loads(
                            task.artifacts
                        )

                    }

                ]

            }

        ]

    }
