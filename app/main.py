import uvicorn
from fastapi import FastAPI

from app.api.endpoints import building


app = FastAPI()

app.include_router(building.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
