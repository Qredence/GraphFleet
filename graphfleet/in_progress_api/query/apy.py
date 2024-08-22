from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from graphrag.config.models.graph_rag_config import GraphRagConfig
from graphrag.query.api import (
    global_search,
    global_search_streaming,
    local_search,
    local_search_streaming,
)

app = FastAPI()

# Assume these are loaded or configured server-side
CONFIG = GraphRagConfig()  # Load your config here
NODES_DF = pd.DataFrame()  # Load your nodes data here
ENTITIES_DF = pd.DataFrame()  # Load your entities data here
COMMUNITY_REPORTS_DF = pd.DataFrame()  # Load your community reports data here
TEXT_UNITS_DF = pd.DataFrame()  # Load your text units data here
RELATIONSHIPS_DF = pd.DataFrame()  # Load your relationships data here
COVARIATES_DF = pd.DataFrame()  # Load your covariates data here
COMMUNITY_LEVEL = 1  # Set your community level here
RESPONSE_TYPE = "text"  # Set your default response type here

class QueryRequest(BaseModel):
    query: str

@app.post("/global_search")
async def api_global_search(request: QueryRequest):
    try:
        # Debug: Print DataFrame info
        print("NODES_DF:", NODES_DF.info())
        print("ENTITIES_DF:", ENTITIES_DF.info())
        print("COMMUNITY_REPORTS_DF:", COMMUNITY_REPORTS_DF.info())

        result = await global_search(
            config=CONFIG,
            nodes=NODES_DF,
            entities=ENTITIES_DF,
            community_reports=COMMUNITY_REPORTS_DF,
            community_level=COMMUNITY_LEVEL,
            response_type=RESPONSE_TYPE,
            query=request.query,
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/global_search_streaming")
async def api_global_search_streaming(request: QueryRequest):
    try:
        # Debug: Print DataFrame info
        print("NODES_DF:", NODES_DF.info())
        print("ENTITIES_DF:", ENTITIES_DF.info())
        print("COMMUNITY_REPORTS_DF:", COMMUNITY_REPORTS_DF.info())

        async def stream_generator():
            async for chunk in global_search_streaming(
                config=CONFIG,
                nodes=NODES_DF,
                entities=ENTITIES_DF,
                community_reports=COMMUNITY_REPORTS_DF,
                community_level=COMMUNITY_LEVEL,
                response_type=RESPONSE_TYPE,
                query=request.query,
            ):
                yield chunk

        return stream_generator()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/local_search")
async def api_local_search(request: QueryRequest):
    try:
        # Debug: Print DataFrame info
        print("NODES_DF:", NODES_DF.info())
        print("ENTITIES_DF:", ENTITIES_DF.info())
        print("COMMUNITY_REPORTS_DF:", COMMUNITY_REPORTS_DF.info())
        print("TEXT_UNITS_DF:", TEXT_UNITS_DF.info())
        print("RELATIONSHIPS_DF:", RELATIONSHIPS_DF.info())
        print("COVARIATES_DF:", COVARIATES_DF.info())

        result = await local_search(
            config=CONFIG,
            nodes=NODES_DF,
            entities=ENTITIES_DF,
            community_reports=COMMUNITY_REPORTS_DF,
            text_units=TEXT_UNITS_DF,
            relationships=RELATIONSHIPS_DF,
            covariates=COVARIATES_DF,
            community_level=COMMUNITY_LEVEL,
            response_type=RESPONSE_TYPE,
            query=request.query,
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/local_search_streaming")
async def api_local_search_streaming(request: QueryRequest):
    try:
        # Debug: Print DataFrame info
        print("NODES_DF:", NODES_DF.info())
        print("ENTITIES_DF:", ENTITIES_DF.info())
        print("COMMUNITY_REPORTS_DF:", COMMUNITY_REPORTS_DF.info())
        print("TEXT_UNITS_DF:", TEXT_UNITS_DF.info())
        print("RELATIONSHIPS_DF:", RELATIONSHIPS_DF.info())
        print("COVARIATES_DF:", COVARIATES_DF.info())

        async def stream_generator():
            async for chunk in local_search_streaming(
                config=CONFIG,
                nodes=NODES_DF,
                entities=ENTITIES_DF,
                community_reports=COMMUNITY_REPORTS_DF,
                text_units=TEXT_UNITS_DF,
                relationships=RELATIONSHIPS_DF,
                covariates=COVARIATES_DF,
                community_level=COMMUNITY_LEVEL,
                response_type=RESPONSE_TYPE,
                query=request.query,
            ):
                yield chunk

        return stream_generator()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)