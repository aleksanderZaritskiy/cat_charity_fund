from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def exc_status_note(obj: Union[CharityProject, Donation]) -> None:
    """
    Установка значений fully_invested и close_date, при
    достижения invested_amount значения равному в full_amount
    как в пожертвованиях так и в проектах.
    """

    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def investing(
    insert_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """
    Ребалансировка значений атрибутов в записях объектов CharityProject, Donation.
    Процесс инвестирования.
    Если создан новый проект, а в базе были «свободные» (не распределённые по
    проектам) суммы пожертвований — они автоматически должны инвестироваться
    в новый проект. То же касается и создания пожертвований: если в момент
    пожертвования есть открытые проекты, эти пожертвования должны автоматически зачислиться на их счета.
    """
    crud = None
    invest_remeins: int = insert_obj.full_amount

    if isinstance(insert_obj, CharityProject):
        crud = donation_crud
        update_objs = await crud.get_open_donations(session)

    if isinstance(insert_obj, Donation):
        crud = charityproject_crud
        update_objs = await crud.get_open_projects(session)

    for cur_obj in update_objs:
        amount: int = cur_obj.full_amount - cur_obj.invested_amount

        if not invest_remeins:
            break

        if invest_remeins > amount:
            invest_remeins -= amount
            cur_obj.invested_amount += amount

        else:
            cur_obj.invested_amount += invest_remeins
            invest_remeins = 0

        await exc_status_note(cur_obj)

    insert_obj.invested_amount = insert_obj.full_amount - invest_remeins
    await exc_status_note(insert_obj)
    await crud.refresh(update_objs + [insert_obj], session)
