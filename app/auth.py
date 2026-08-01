from fastapi import Header, HTTPException


def authenticate(
    authorization: str | None = Header(None)
):

    if not authorization:
        raise HTTPException(
            401,
            "Unauthorized"
        )


    if not authorization.startswith("Bearer "):
        raise HTTPException(
            401,
            "Unauthorized"
        )


    return authorization.split(
        " ",
        1
    )[1]