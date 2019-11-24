import os

class Config:
    SECRET_KEY='amos'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ermoh:12345@localhost/pitch'
    UPLOADED_PHOTOS_DEST='app/static/photos'

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig

}