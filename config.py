# Development Configuration

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    POSTGRES = {
        'user': 'postgres',
        'pw': 'vidyut2019*',
        'db': 'vidyut2019',
        'host': '10.0.0.139',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'motham-padithamaanallooo'
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'no-reply@vidyut.amrita.edu'
    MAIL_PASSWORD = 'amma@123'
    MAIL_DEFAULT_SENDER = 'no-reply@vidyut.amrita.edu'
    MAIL_MAX_EMAILS = 3000
    HOST_LOC = 'production'
    DEVELOPMENT = True
    DEBUG = True
    MAINTENANCE = False
    JSON_SORT_KEYS = False

    # ACRD
    ACRDEND = 'https://payments.acrd.org.in/pay/makethirdpartypayment'
    PURPOSE = 'VIDYUT19TEST'
    PROBURL = 'https://payments.acrd.org.in/pay/doubleverifythirdparty'
    PAYCODE = 'VIDYUT19TEST'
    ACRDKEY = 'WEGSNGOXHEUDEEDD'
    ACRDIV = '3564234432724374'

class TestingConfig(Config):
    TESTING = True
