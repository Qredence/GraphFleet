from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
async def example_endpoint():
    return {"message": "This is an example v1 endpoint"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}