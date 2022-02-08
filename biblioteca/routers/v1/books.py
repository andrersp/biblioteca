# -*- coding: utf-8 -*-

from http.client import responses
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from biblioteca.core.http_responses import success, error
from biblioteca.models.livro import ModelLivro, ModelLivroBase
from biblioteca.ext.database import get_session
from biblioteca.crud import books as crud_book


router = APIRouter(tags=['Books'], prefix='/books')


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


@router.get("",  response_model=list[ModelLivro],  responses=response_schema)
async def get_livros(session: AsyncSession = Depends(get_session)):
    books = await crud_book.get_all_books(session)
    return success({"data": books})


@router.post("", responses=create_response)
async def create_book(data: ModelLivroBase, session=Depends(get_session)):

    book = await crud_book.create_book(session, data)

    return success(book.dict(), status_code=201)

    return book
