from pydantic import BaseModel


# 입력받아서 테이블에 저장될 클래스
class NoteIn(BaseModel):
    text: str
    completed: bool


# 데이터 검색 등의 요청을 받았을 때 response로 반환될 클래스
class NoteResponse(BaseModel):
    id: int
    text: str
    completed: bool
