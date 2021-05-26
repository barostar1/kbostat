import os

BASE_DIR = os.path.dirname(__file__)
homedir = os.path.dirname(os.path.realpath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'kbostat.db'))
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://hankyungedudb006:gksrud86438!@my8001.gabiadb.com:3306/hankyung006'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'dev'
