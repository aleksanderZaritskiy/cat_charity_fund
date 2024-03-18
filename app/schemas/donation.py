from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class DonationBase(BaseModel):

    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationtDB(DonationBase):

    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
