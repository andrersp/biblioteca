# -*- coding: utf-8 -*-

from fastapi import FastAPI

from biblioteca.routers.v1.obras import router as router_books


def init_app(app: FastAPI):
    app.include_router(router_books, prefix="/v1")
