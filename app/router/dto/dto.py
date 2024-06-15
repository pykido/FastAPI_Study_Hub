from pydantic import BaseModel


class CreateNoteDTO(BaseModel):
    text: str
    completed: bool

class UpdateNoteDTO(BaseModel):
    text: str
    completed: bool
