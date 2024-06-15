from typing import List

from fastapi import APIRouter

from fastapiStudyHub.app.model.model import NoteResponse
from fastapiStudyHub.app.router.dto.dto import CreateNoteDTO, UpdateNoteDTO
from fastapiStudyHub.app.service.note_service import create_note, read_notes, update_note, delete_note

note_router = APIRouter()

@note_router.post("/notes/", response_model=NoteResponse)
async def create_note_api(dto: CreateNoteDTO):
    return await create_note(
        text = dto.text,
        completed = dto.completed
    )


@note_router.get("/notes/", response_model=List[NoteResponse])
async def read_notes_api():
    return await read_notes()


@note_router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note_api(note_id: int, dto: UpdateNoteDTO):
    return await update_note(
        note_id = note_id,
        text = dto.text,
        completed = dto.completed
    )


@note_router.delete("/notes/{note_id}")
async def delete_note_api(note_id: int):
    return await delete_note(note_id)
