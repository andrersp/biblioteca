# -*- coding: utf-8 -*-

from sqlmodel import SQLModel, Field


class ModelLivroBase(SQLModel):
    titulo: str
    editora: str
    foto: str


class ModelLivro(ModelLivroBase, table=True):
    id: int | None = Field(None, primary_key=True)
