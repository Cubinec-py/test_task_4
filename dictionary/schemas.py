from pydantic import BaseModel, ConfigDict


class DictionaryRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class DictionaryCreate(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
