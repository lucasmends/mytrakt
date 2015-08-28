from mongoengine import *
from urllib.error import HTTPError
from api import model_api, settings
from api.errors import *
from api.base_classes import *
from datetime import date, timedelta
from django.utils.functional import cached_property



class Episodes():

	def __init__(self, season_id_pk):
		episodes = Episode.objects(season_id_pk = season_id_pk)
		self.__episodes = []
		for episode in _episodes:
			self.__episodes.append(episode)
		self.__shellSort()

	def __iter__(self):
		return self.__episodes

	def __getitem__(self,index):
		return self.__episodes[index - 1]

	def __shellSort(self):
		inc = len(self.__episodes) // 2
		while inc:
			for i in range(0, len(self.__episodes)):
				j = i
				temp = self.__episodes[i]
				while j >= inc and self.__episodes[j - inc].number  > temp.number:
					self.__episodes[j] = self.__episodes[j - inc]
					j -= inc
			self.__episodes[j] = temp
		inc = inc // 2 if inc // 2 else (0 if inc == 1 else 1)


# Create your models here.

class Movie(BaseDocumment):

	"""docstring for Movie"""
	def __init__(self, id):
		try:
			self = Movie.objects.get(id=id)
			now = datetime.now()
			if (now - self.__date_update).days > settings.UPDATE_FREQUENCY:
				movie_from_api = model_api.Movie(id, images =False)
				self.__update_attr(movie_from_api)
				self.save()

		except DoesNotExist:
			try:
				movie_from_api = model_api.Movie(id, images =True)
				self.__update_attr(movie_from_api)
				self.__update_images(movie_from_api)
				self.save()
			except HTTPError:
				raise NotFoundError(value="movie")

		except MultipleObjectsReturned:
			Movie.objects(id=id).delete()
			movie_from_api = model_api.Movie(id, images =True)
			self.__update_attr(movie_from_api)
			self.__update_images(movie_from_api)
			self.save()
# filme deletado
#		except HTTPError:
#			rating NotFoundError(value="movie")

	def __update_attr(self, movie_from_api):
		self.title = movie_from_api['title']
		self.year = movie_from_api['year']
		self.overview = movie_from_api['overview']
		self.rating = movie_from_api['rating']
		self.votes = movie_from_api['votes']
		self.__date_update = date.today()
		
		self.ids = ID()
		self.ids.trakt = movie_from_api['ids']['trakt']
		self.ids.imdb = movie_from_api['ids']['imdb']
		self.ids.slug = movie_from_api['ids']['slug']

	def __update_images(self, movie_from_api):
		self.images = {}
		self.images['fanart'] = movie_from_api['fanart']
		self.images['poster'] = movie_from_api['poster']





class Episode(BaseDocumentIntern):
	season_id_pk = ObjectIdField(required=True)

	"""docstring for Episode
		show_id não é ObjectIdField"""
	def __init__(self, show_id, season, number):
		season = Season(show_id = show_id, season = season)
		try:
			episode = Episode.objects.get(season_id_pk = season.pk, number = number)
			now = datetime.now()
			if (now - self.__date_update).days > settings.UPDATE_FREQUENCY:
				episode_from_api = model_api.Episode(show_id = show_id, season_number = season, episode_number = number)
				self.__update_attr(episode_from_api)
				self.save()

		except DoesNotExist:
			try:
				episode_from_api = model_api.Episode(show_id = show_id, season_number = season, episode_number = number, images = True)
				self.season_id_pk = season.pk
				self.__update_attr(episode_from_api)
				self.__update_image(episode_from_api)
				self.save()
			except HTTPError:
				raise NotFoundError(value="episode")

		except MultipleObjectsReturned:
			Episode.objects(season_id_pk = season.pk, number = number).delete()
			self.season_id_pk = season.pk
			self.__update_attr(episode_from_api)
			self.__update_image(episode_from_api)
			self.save()			
# episodio deletado
#		except HTTPError:
#			raise NotFindException(value="episode")
			
	@cached_property
	def season(self):
		if not hasattr(self, '_season'):
			self._season = Season.objects.get(pk = self.season_id_pk)
		return self._season

	@cached_property
	def show(self):
		if not hasattr(self, '_show'):
			self._show = Show.objects.get(pk = self.season.show_id_pk)
		return self._show

	def __update_attr(self, episode_from_api):
		self.number = episode_from_api['number']
		self.overview = episode_from_api['overview']
		self.rating = episode_from_api['rating']
		self.votes = episode_from_api['votes']
		self.__date_update = date.today()
		
		self.ids = ID()
		self.ids.trakt = episode_from_api['ids']['trakt']
		self.ids.imdb = episode_from_api['ids']['imdb']

	def __update_image(self, episode_from_api):
		self.images = episode_from_api['image']

class Season(BaseDocumentIntern):
	show_id_pk = ObjectIdField(required=True)
	episode_count = IntField(required=True)
	aired_episodes = IntField(required=True)

	"""docstring for Season
		show_id não pe ObjectIdField"""
	def __init__(self, show_id, season):
		show = Show(show_id)
		try:
			self = Season.objects.get(show_id_pk = show.pk, number = season)
			now = datetime.now()
			if (now - self.__date_update).days > settings.UPDATE_FREQUENCY:
				season_from_api = model_api.Season(show_id = show_id, season_number = season)
				self.__update_attr(season_from_api)
				self.save()
		except DoesNotExist:
			try:
				season_from_api = model_api.Season(show_id = show_id, season_number = season, images = True)
				self.__update_attr(season_from_api)
				self.__update_image(season_from_api)
				self.show_id_pk = show.pk
				self.save()
			except HTTPError:
				raise NotFoundError(value="season")

	@cached_property
	def episodes(self):
		if not hasattr(self, '_episodes'):
			self._episodes = Episodes(season_id_pk = self.pk)
		return self._episodes

	@cached_property
	def show(self):
		if not hasattr(self, '_show'):
			self._show = Show.objects.get(pk = self.show_id_pk)
		return self._show

	def __update_attr(self, season_from_api):
		self.number = season_from_api['number']
		self.overview = season_from_api['overview']
		self.rating = season_from_api['rating']
		self.votes = season_from_api['votes']
		self.episode_count = season_from_api['episode_count']
		self.aired_episodes = season_from_api['aired_episodes']
		self.__date_update = date.today()

		self.ids = ID()
		self.ids.trakt = season_from_api['ids']['trakt']
		self.ids.imdb = season_from_api['ids']['imdb']

	def __update_episodes(self, season_from_api):
		for i in range(1, self.episode_count + 1):
			self.episodes[i] = Episode(show_id, season, i)

	def __update_image(self, season_from_api):
		self.image = season_from_api['image']
		

class Seasons():

	"""docstring for Seasons
		show_id não é ObjectIdField"""
	def __init__(self, show_id):
		show = Show(show_id)
		try:
			seasons = Season.objects(show_id_pk = show.pk)
			#self.show_id é ObjectIdField
			self.show_id_pk = seasons[0].show_id_pk
			self.seasons = []
			for season in seasons:
				self.seasons.append(season)
			self.__shellSort()
			self.number_season = len(self.seasons)
		
		except DoesNotExist:
			self.number_season = len(api_seasons)
			Seasons.update(show_id = show_id)
			#perigoso, potencial loop
			self = Seasons(show_id = show_id)

	def __getitem__(self,index):
		return self.seasons[index]

	def __iter__(self):
		return self.seasons

	@staticmethod
	def update(show_id):
		api_seasons = model_api.Seasons(show_id = show_id, images = False, extended = False)
		for season in api_seasons:
			Season(show_id = show_id, season = season['number']) 

	@cached_property
	def show(self):
		if not hasattr(self, '_show'):
			self._show = Show.objects.get(pk = self.show_id_pk)
		return self._show

	def __shellSort(self):
		inc = len(self.seasons) // 2
		while inc:
			for i in range(0, len(self.seasons)):
				j = i
				temp = self.seasons[i]
				while j >= inc and self.seasons[j - inc].number  > temp.number:
					self.seasons[j] = self.seasons[j - inc]
					j -= inc
			self.seasons[j] = temp
		inc = inc // 2 if inc // 2 else (0 if inc == 1 else 1)

class Show(BaseDocumment):

	"""docstring for Show"""
	def __init__(self, id):
		try:
			self = Show.objects.get(id=id)
			delta_time = (datetime.now() - self.__date_update).days
			if delta_time > settings.UPDATE_FREQUENCY:
				show_from_api = model_api.Movie(id, images =False)
				self.__update_attr(show_from_api)
				self.save()
			if delta_time > ( settings.UPDATE_FREQUENCY // 2 ):
				Seasons.update(show_id = id)

		except DoesNotExist:
			try:
				show_from_api = model_api.Show(id, images =True)
				self.__update_attr(show_from_api)
				self.__update_images(show_from_api)
				self.save()
			except HTTPError:
				raise NotFoundError(value="show")

		except MultipleObjectsReturned:
			Show.objects(id = id).delete()
			show_from_api = model_api.Show(id, images =True)
			self.__update_attr(show_from_api)
			self.__update_images(show_from_api)
			self.save()

	@cached_property
	def seasons(self):
		if not hasattr(self, '_seasons'):
			self._seasons = Seasons(show_id = self.ids.slug)
		return self._seasons

	def __update_attr(self, show_from_api):
		self.title = show_from_api['title']
		self.year = show_from_api['year']
		self.overview = show_from_api['overview']
		self.rating = show_from_api['rating']
		self.votes = show_from_api['votes']
		self.__date_update = date.today()
		
		self.ids = ID()
		self.ids.trakt = show_from_api['ids']['trakt']
		self.ids.imdb = show_from_api['ids']['imdb']
		self.ids.slug = show_from_api['ids']['slug']

	def __update_images(self, show_from_api):
		self.images = {}
		self.images['fanart'] = show_from_api['fanart']
		self.images['poster'] = show_from_api['poster']

