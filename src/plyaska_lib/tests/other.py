import json

from httpx import Response


def output_response(response: Response):
    return (
        f"Output response:{json.dumps(response.json(), indent=4)}\n"
        f"Output request:{json.dumps(response.request.content.decode('utf-8'), indent=4)}"
    )
