import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_padrao")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Banco padrão (SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///matchmovies.db"
    )


class DevelopmentConfig(Config):
    DEBUG = True

    # Em desenvolvimento usamos SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///matchmovies_dev.db"
    )


class ProductionConfig(Config):
    DEBUG = False

    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///matchmovies_prod.db"
    )

