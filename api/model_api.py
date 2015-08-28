from urllib.request import Request, urlopen
import json
from api import settings
from api.images import get_images_serie, get_images_seasons, get_images_season, get_images_episode, get_images_movie


def Movie(id, images = False, extended = True):
	url = settings.URL + '/movies/' + id + ('?extended=full' if extended else None)
	request = Request(url, headers=settings.HEADER)
	response = urlopen(request).read().decode('utf-8')
	movie = json.loads(response)
	
	if images:
		url = settings.URL + '/movies/' + id + '?extended=images'
		request = Request(url, headers=settings.HEADER)
		response = urlopen(request).read().decode('utf-8')
		movie = get_images_movie(movie, json.loads(response))

	return movie
		

def Show(id, images = False, seasons = False, extended = True):
	url = settings.URL + '/shows/' + id + ('?extended=full' if extended else None)
	request = Request(url, headers=settings.HEADER)
	response = urlopen(request).read().decode('utf-8')
	show = json.loads(response)

	if images:
		url = settings.URL + '/shows/' + id + '?extended=images'
		request = Request(url, headers=settings.HEADER)
		response = urlopen(request).read().decode('utf-8')
		show = get_images_serie(show, json.loads(response))

	if seasons:
		show['seasons'] = Seasons(id, images, extended)

	return show


def Seasons(show_id, images = True, extended = True):
	url = settings.URL + '/shows/' + show_id + '/seasons' + ('?extended=full' if extended else  None)
	request = Request(url, headers=settings.HEADER)
	response = urlopen(request).read().decode('utf-8')
	seasons = json.loads(response)
	
	if images:
		url = settings.URL + '/shows/' + show_id + '/seasons?extended=images'
		request = Request(url, headers=settings.HEADER)
		response = urlopen(request).read().decode('utf-8')
		seasons = get_images_seasons(seasons, json.loads(response))

	return seasons


def Season(show_id, season_number, images = False, episodes = False):
	seasons = Seasons(show_id, images)
	season = seasons[season_number]

	if images:
		url = settings.URL + '/shows/' + show_id + '/seasons?extended=images'
		request = Request(url, headers=settings.HEADER)
		response = urlopen(request).read().decode('utf-8')
		season = get_images_season(season, json.loads(response))

	if episodes:
		season['episodes'] = []
		for i in range(1, season['episode_count'] + 1):
			season['episodes'].append(Episode(show_id, season_number, i, images))

	return season


def Episode(show_id, season_number, episode_number, images = False, extended = True):
	url = settings.URL + '/shows/' + show_id + '/seasons/' + str(season_number)+ '/episodes/' + str(episode_number) + ('?extended=full' if extended else None)
	request = Request(url, headers=settings.HEADER)
	response = urlopen(request).read().decode('utf-8')
	episode = json.loads(response)

	if images:
		url = settings.URL + '/shows/' + show_id + '/seasons/' + str(season_number)+ '/' + str(episode_number) + '?extended=images'
		request = Request(url, headers=settings.HEADER)
		response = urlopen(request).read().decode('utf-8')
		episode = get_images_episode(episode, json.loads(response))

	return episode
