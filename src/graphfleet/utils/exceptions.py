from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

class GraphFleetException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

async def graphfleet_exception_handler(request: Request, exc: GraphFleetException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "type": "GraphFleetException",
            "path": request.url.path
        }
    )