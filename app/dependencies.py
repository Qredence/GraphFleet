from fastapi import Depends
from app.services.graphfleet import GraphFleet, get_graphfleet

def get_graphfleet_service():
    return Depends(get_graphfleet)