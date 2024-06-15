from typing import List

from fastapiStudyHub.app.model.model import NoteIn, NoteResponse
from fastapiStudyHub.app.repository.repository import NoteRepository


async def create_note(text: str, completed: bool):
    noteResponse = NoteIn(
        text=text,
        completed=completed
    )

    return await NoteRepository().create(
        note = noteResponse
    )


async def read_notes() -> List[NoteResponse]:
    return await NoteRepository().read_all()


async def update_note(note_id: int, text: str, completed: bool):
    note = NoteIn(
        text=text,
        completed=completed
    )
    return await NoteRepository().update(note_id, note)


async def delete_note(note_id: int):
    return await NoteRepository().delete(note_id)
