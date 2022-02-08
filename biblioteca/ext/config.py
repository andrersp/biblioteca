# -*- coding: utf-8 -*-
from importlib import import_module
from biblioteca.ext.settings import settings


def init_app(app):
    app.title = "Biblioteca"
    for extension in settings.EXTENSIONS:
        mod = import_module(extension)
        mod.init_app(app)
