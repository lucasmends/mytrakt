def get_images_movie(movie, data):
	images = {}
	images['fanart'] = data['images']['fanart'].get('medium')
	images['poster'] = data['images']['poster'].get('thumb')
	# Search if the images are on cache, if not put them on
	movie['images'] = images
	return movie

def get_images_serie(serie, data):
	images = {}
	images['fanart'] = data['images']['fanart'].get('medium')
	images['poster'] = data['images']['poster'].get('thumb')
	# Search if the images are on cache, if not put them on
	serie['images'] = images
	return serie

def get_images_seasons(seasons, data):
	for i in range(0, len(seasons)):
		image = data[i]['images']['poster'].get('thumb')
		# Search if the images are on cache, if not put them on
		seasons[i]['image'] = image
	return seasons
	
def get_images_season(season, data):
	i = season['number']
	image = data[i]['images']['poster'].get('thumb')
	# Search if the images are on cache, if not put them on
	season['image'] = image
	return season

def get_images_episode(episode, data):
	image = data['images']['screenshot'].get('thumb')
	# Search if the images are on cache, if not put them on
	episode['image'] = image
	return episode