# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from biblioteca.models.livro import ModelLivro, ModelLivroBase


async def create_book(session: AsyncSession, data: ModelLivroBase):
    book = ModelLivro(**data.dict())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_all_books(session: AsyncSession) -> list[ModelLivro]:

    query = select(ModelLivro)
    result = await session.execute(query)

    return _serialize_songs(result.scalars().all())


def _serialize_songs(songs: list[ModelLivro]):

    return list(map(lambda x: {
        "id": x.id,
        "titulo": x.titulo,
        "editora": x.editora,
        "foto": x.foto
    }, songs))
