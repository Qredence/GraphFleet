from typing import Any, Dict, List, Tuple, AsyncGenerator, Union, cast
from fastapi import FastAPI, HTTPException
from src.graphfleet.graphfleet import GraphFleet
from pandas import DataFrame

app = FastAPI()

graph_fleet = GraphFleet()

@app.get("/global-search")
async def global_search(query: str) -> Tuple[str, Dict[str, List[Dict[str, Any]]]]:
    try:
        result, confidence = graph_fleet.query(query, method="global")
        context_data = _reformat_context_data(result)
        return result, context_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global search error: {str(e)}")

@app.get("/global-search-streaming")
async def global_search_streaming(query: str) -> AsyncGenerator[Union[str, DataFrame], None]:
    try:
        result, _ = graph_fleet.query(query, method="global")
        yield result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global search streaming error: {str(e)}")

@app.get("/local-search")
async def local_search(query: str) -> Tuple[str, Dict[str, List[Dict[str, Any]]]]:
    try:
        result, confidence = graph_fleet.query(query, method="local")
        context_data = _reformat_context_data(result)
        return result, context_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local search error: {str(e)}")

@app.get("/local-search-streaming")
async def local_search_streaming(query: str) -> AsyncGenerator[Union[str, DataFrame], None]:
    try:
        result, _ = graph_fleet.query(query, method="local")
        yield result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local search streaming error: {str(e)}")

def _reformat_context_data(context_data: Union[str, List[DataFrame], Dict[str, DataFrame]]) -> Dict[str, Any]:
    if isinstance(context_data, str):
        return {"data": context_data}
    elif isinstance(context_data, list):
        return {"data": [df.to_dict(orient='records') for df in context_data]}
    else:
        return context_data
