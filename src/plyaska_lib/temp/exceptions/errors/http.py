from fastapi import HTTPException


class NotFoundedHTTPException(HTTPException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message=None):
        if message:
            message = f" {message}"
        message = f"Not found{message}"
        super().__init__(status_code=404, detail=message)
