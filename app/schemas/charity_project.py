from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator, Extra


class CharityProjectBase(BaseModel):

    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]

    @validator('name')
    def name_cannot_be_null(cls, value):
        if not value or not value.strip():
            raise ValueError('Укажите имя проекта')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):

        if not value or not value.strip():
            raise ValueError('Укажите описание проекта')
        return value

    @root_validator(skip_on_failure=True)
    def check_eq_name_desc(cls, values):
        name, desc = values['name'], values['description']
        if name and desc and name == desc:
            raise ValueError(
                'Название проекта и описание не могут быть одинаковы'
            )
        return values

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Название проекта',
        description='любой регистр, максимум 100 символов',
    )
    description: str = Field(
        ...,
        min_length=1,
        title='Описание проекта',
        description='минимум 1 символ',
    )
    full_amount: int = Field(
        ..., gt=0, title='Необходимая сумма', description='значение выше 0'
    )


class CharityProjectUpdate(CharityProjectBase):
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
