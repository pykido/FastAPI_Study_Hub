from fastapi import FastAPI
from fastapiStudyHub.app.database import db
from fastapiStudyHub.app.router.note_router import note_router

app = FastAPI()

# note_router를 app에 추가
app.include_router(note_router)

# FastAPI 애플리케이션이 시작될 때 호출됨
@app.on_event("startup")
async def startup():
    await db.database.connect()


# FastAPI 애플리케이션이 종료될 때 호출
@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()

