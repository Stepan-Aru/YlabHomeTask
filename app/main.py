from fastapi import FastAPI, Request, Response

from app.database import SessionLocal
from app.routes import router

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        await request.state.db.close()
    return response


app.include_router(router=router, prefix="/api/v1")
