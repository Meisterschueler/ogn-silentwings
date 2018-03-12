import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    NAVITER_CLIENT_ID = '1891_NMSBsbSEAstIlKR5T3KKOAbzrQt0rPa6q6J0rBEE'
    NAVITER_SECRET = '1l7HJT1pu8Y5iJVtXe9irlP3v0yW4!Qg..Ia7RLOdIf51JZUQ9hSFsrgTo3.g4IH'
    NAVITER_BASE_URL = 'http://api.test.soaringspot.com/v1/'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    NAVITER_CLIENT_ID = '1891_NMSBsbSEAstIlKR5T3KKOAbzrQt0rPa6q6J0rBEE'
    NAVITER_SECRET = '1l7HJT1pu8Y5iJVtXe9irlP3v0yW4!Qg..Ia7RLOdIf51JZUQ9hSFsrgTo3.g4IH'
    NAVITER_BASE_URL = 'http://api.test.soaringspot.com/v1/'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    NAVITER_CLIENT_ID = '2470_A!6LMHu8oxdHC8CFU8lxW.LyykzdgZjGTTXeTwU3'
    NAVITER_SECRET = 'Tlfd3bDcmCV3AkNhZEygmTDXaLYH6APLvDokwjj9RilSvrkCFmLhxi331TPsrUH0'
    NAVITER_BASE_URL = 'http://api.soaringspot.com/v1/'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
