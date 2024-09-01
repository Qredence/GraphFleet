from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

class GraphFleetException(CustomException):
    pass

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

async def graphfleet_exception_handler(request: Request, exc: GraphFleetException):
    return JSONResponse(
        status_code=400,
        content={"message": f"GraphFleet error: {exc.name}"},
    )

def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(GraphFleetException, graphfleet_exception_handler)