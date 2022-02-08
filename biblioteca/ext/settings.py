import os
import pathlib
from functools import lru_cache


class BaseConfig:

    DATABASE_CONNECT_DICT: dict = {}
    EXTENSIONS = ['biblioteca.routers.v1',
                  'biblioteca.ext.database',
                  'biblioteca.ext.cors'

                  ]


class DevelopmentConfig(BaseConfig):
    DATABASE_URL: str = 'postgresql+asyncpg://biblioteca:biblioteca@db/biblioteca'
    pass


class ProductionConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get("SQLALCHEMY_DATABASE_URI")
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
