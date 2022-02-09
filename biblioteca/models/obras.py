# -*- coding: utf-8 -*-

from typing import Optional
from sqlmodel import SQLModel, Field, ARRAY, String, Relationship
from pydantic import BaseModel
from sqlalchemy.orm import relationship


class SchemaObras(BaseModel):
    titulo: str
    editora: str
    foto: str
    autores: list[str]


class ModelObrasBase(SQLModel):
    titulo: str
    editora: str
    foto: str


class ModelObras(ModelObrasBase, table=True):
    __tablename__ = 'obras'
    id: int | None = Field(None, primary_key=True)
    autores: Optional['ModelAutores'] = Relationship(
        sa_relationship=relationship('ModelAutores', cascade="all, delete", back_populates='obras'))


class ModelAutores(SQLModel, table=True):
    __tablename__ = 'autores'
    id: int | None = Field(None, primary_key=True)
    name: str
    id_obra: int | None = Field(None, foreign_key='obras.id')
    obras: Optional['ModelObras'] = Relationship(back_populates='autores')
