from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./FASTAPI_pykido.db"	# database의 url

# 만약 PostgreSQL같은 다른 SQL을 사용한다면 다른 DATABASE_URL을 사용해야 함!
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

# DATABASE_URL에 database 객체를 생성
database = databases.Database(DATABASE_URL)

# SQLAlchemy로부터 메타데이터 생성
metadata = sqlalchemy.MetaData()

# notes 테이블 생성
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

# SQLAlchemy 엔진 생성
## SQLite를 DB로 사용하자
## SQLite는 기본적으로 멀티 스레드 환경에서 DB 접근을 허용하지 않기에 멀티 스레드 접근을 허용하도록 설정
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
## metadata 객체가 포함된 모든 테이블들을 실제 DB에 생성. 즉, notes 테이블을 DB에 생성
metadata.create_all(engine)


# 입력받아서 테이블에 저장될 클래스
class NoteIn(BaseModel):
    text: str
    completed: bool


# 데이터 검색 등의 요청을 받았을 때 response로 반환될 클래스
class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()

# FastAPI 애플리케이션이 시작될 때 호출됨
@app.on_event("startup")
async def startup():
    await database.connect()

# FastAPI 애플리케이션이 종료될 때 호출
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


## 1. CREATE
@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}
    # **note.dict(): Python unpack 문법
    # note에 "id" key를 추가하여 response로 반환!

## 2. READ
# /notes에 GET 요청을 보내면 현재 테이블의 모든 데이터를 반환!
@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)
    # return type: List[Note]

## 3. UPDATE
@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, note: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(text=note.text, completed=note.completed)
    await database.execute(query)
    return {**note.dict(), "id": note_id}

## 4. DELETE
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": "Note deleted successfully!"}



