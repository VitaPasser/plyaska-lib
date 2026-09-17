class NotFoundedError(Exception):
    def __init__(self, detail: str):
        self.detail = f"Not founded: {detail}"
