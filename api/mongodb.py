from mongoengine import *
from api import settings

def start_db():
	connect(settings.DATABASE, username=settings.USER, password=settings.PASSWORD, host=settings.HOST, port=settings.PORT)