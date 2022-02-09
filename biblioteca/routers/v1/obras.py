# -*- coding: utf-8 -*-

from http.client import responses
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from biblioteca.core.http_responses import success, error
from biblioteca.models.obras import ModelObras, ModelObrasBase, SchemaObras
from biblioteca.ext.database import get_session
from biblioteca.crud import obras as crud_book


router = APIRouter(tags=['Books'], prefix='/obras')


create_response = {
    201: {
        "description": "Create Success",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "id": "Id",
                    "titulo": "string",
                    "editora": "string",
                    "foto": "url"

                },

            }
        },
    }
}

response_schema = {

    200: {
        "description": "Lista todos os livros",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": [{
                        "id": "Id",
                        "titulo": "string",
                        "editora": "string",
                        "foto": "url"
                    }]
                },

            }
        },
    },
    400: {
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "detail": [
                        {
                            "msg": "mensagem de erro",
                            "type": "error_tyle"
                        }

                    ]
                }
            }
        }
    },
    500: {
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "detail": [
                        {
                            "msg": "Internal Error",
                            "type": "internal_error"
                        }

                    ]

                }
            }
        }
    }



}


@router.get("",  response_model=list[ModelObras],  responses=response_schema)
async def get_livros(session: AsyncSession = Depends(get_session)):
    obras = await crud_book.get_all_books(session)
    return success({"data": obras})


@router.get("/{id_obra}")
async def select_obra(id_obra: int, session: AsyncSession = Depends(get_session)):

    obra = await crud_book.select_obra(session, id_obra)

    if not obra:
        return error(status_code=404)

    return success(obra)


@router.post("", responses=create_response)
async def create_book(data: SchemaObras, session=Depends(get_session)):

    try:
        book = await crud_book.create_book(session, data)
    except Exception:
        return error(status_code=500)
    else:
        book = await crud_book.select_obra(session, book)

    return success(book, status_code=201)
