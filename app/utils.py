import json
import hashlib



def hash_message(data):

    text=json.dumps(
        data,
        sort_keys=True,
        separators=(
            ",",
            ":"
        )
    )


    return hashlib.sha256(
        text.encode()
    ).hexdigest()