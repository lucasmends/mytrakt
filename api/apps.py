from django.apps import AppConfig
from api.mongodb import *

class API(AppConfig):

	name = 'api'
	verbose_name = "API for trakt"

	def ready(self):
		print("Connect MongoDB")
		start_db()