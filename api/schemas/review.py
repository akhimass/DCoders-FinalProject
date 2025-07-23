from pydantic import BaseModel

class ReviewBase(BaseModel):
    menu_item_id: int
    score: int
    text: str

class ReviewCreate(ReviewBase):
    pass

class ReviewRead(ReviewBase):
    id: int

    class Config:
        orm_mode = True