from typing import List

from fastapiStudyHub.app.database.db import database, notes
from fastapiStudyHub.app.model.model import NoteIn, NoteResponse


class NoteRepository:
    ## 1. CREATE
    async def create(self, note: NoteIn):
        query = notes.insert().values(text=note.text, completed=note.completed)
        last_record_id = await database.execute(query)

        return {**note.dict(), "id": last_record_id}
        # **note.dict(): Python unpack 문법
        # note에 "id" key를 추가하여 response로 반환!

    ## 2. READ
    # /notes에 GET 요청을 보내면 현재 테이블의 모든 데이터를 반환!
    async def read_all(self) -> List[NoteResponse]:
        query = notes.select()

        return await database.fetch_all(query)
        # return type: List[Note]

    ## 3. UPDATE
    async def update(self, note_id: int, note: NoteIn):
        query = notes.update().where(notes.c.id == note_id).values(text=note.text, completed=note.completed)
        await database.execute(query)

        return {**note.dict(), "id": note_id}

    ## 4. DELETE
    async def delete(self, note_id: int):
        query = notes.delete().where(notes.c.id == note_id)
        await database.execute(query)

        return {"message": "Note deleted successfully!"}
