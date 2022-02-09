# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from biblioteca.models.obras import ModelObras, ModelObrasBase, SchemaObras, ModelAutores


async def create_book(session: AsyncSession, data: SchemaObras):
    autores = [ModelAutores(name=x) for x in data.autores]
    book = ModelObras(**data.dict(exclude={'autores', }), autores=autores)
    session.add(book)

    await session.commit()
    await session.refresh(book)

    return book.id


async def select_obra(session: AsyncSession, id: int) -> ModelObras:
    obra = await session.get(ModelObras, id, options=(selectinload(ModelObras.autores),))

    if not obra:
        return False
    return _serialize_obra(obra)


async def delete_obra(session: AsyncSession, id: int) -> bool:

    obra = await session.get(ModelObras, id)

    if obra:
        await session.delete(obra)
        await session.commit()
        return True
    return False


async def get_all_books(session: AsyncSession) -> list[ModelObras]:

    query = select(ModelObras).options(selectinload(ModelObras.autores),)
    result = await session.execute(query)

    return _serialize_obras(result.scalars().all())


def _serialize_obras(obras: list[ModelObras]):

    return list(map(lambda x: {
        "id": x.id,
        "titulo": x.titulo,
        "editora": x.editora,
        "foto": x.foto,
        "autores": list(map(lambda z: z.name, x.autores))
    }, obras))


def _serialize_obra(obra: list[ModelObras]):

    return {
        "id": obra.id,
        "titulo": obra.titulo,
        "editora": obra.editora,
        "foto": obra.foto,
        "autores": list(map(lambda z: z.name, obra.autores))
    }
