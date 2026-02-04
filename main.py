from typing import Optional
from fastapi import FastAPI
from db import Base, engine
from api.evaluation import router as evaluation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Evaluation API")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

app.include_router(evaluation_router)
