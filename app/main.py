
from fastapi import FastAPI
from .database import engine, Base, init_redis, close_redis
from .routes import user, task

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(task.router)

@app.get("/")
def read_root():
    return {"message": "Task API"}

@app.on_event("startup")
async def startup_event():
    await init_redis()

@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()


