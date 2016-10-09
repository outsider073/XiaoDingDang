class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class DevelopmentConfig(Config):
    DEBUG = True