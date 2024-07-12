import os
import logging

from logging.handlers import SysLogHandler


basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    APP_NAME = os.environ.get('APP_NAME')
    DEBUG = os.environ.get('DEBUG')
    TESTING = True
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'
    PORT = os.environ.get('PORT') if os.environ.get('PORT') else 8000

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @staticmethod
    def init_app(app):
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'

        # Log to syslog
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = Config
