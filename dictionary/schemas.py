from pydantic import BaseModel


class DictionaryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DictionaryCreate(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
