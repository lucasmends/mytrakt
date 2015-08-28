from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from api.models import Show, Seasons, Season, Episode
from api.errors import NotFoundError

# Create your views here.

def show(request, id):
	try:
		show = Show(id)
	except NotFoundError as e:
		raise HttpResponseNotFound()
	if request.method == "GET":
		return render(request, 'show.html', {'show': show})

def seasons(request, show_id):
	try:
		seasons = Show(show_id).seasons
	except NotFoundError as e:
		raise HttpResponseNotFound()
	if request.method == "GET":
		return render(request, 'seasons.html', {'seasons': seasons})	

def season(request, show_id, number):
	try:
		season = Season(show_id = show_id, season = number)
	except NotFoundError as e:
		raise HttpResponseNotFound()
	if request.method == "GET":
		return render(request, 'season.html', {'season': season})

def episode(request, show_id, season_number, number):
	try:
		episode = Episode(show_id = show_id, season = season_number, number = number)
	except NotFoundError as e:
		raise HttpResponseNotFound()
	if request.method == "GET":
		return render(request, 'episode.html', {'episode': episode})
	

