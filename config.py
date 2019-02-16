class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///a1_db.sqlite"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///a1_db.sqlite"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///a1_db.sqlite"