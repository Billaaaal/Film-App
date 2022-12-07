from django.shortcuts import render
from datetime import datetime
import requests, json
import math
import locale
from datetime import date
import time
import datetime
import os
import math
import webbrowser
import re

api_key = "0185061fa528877524ccec88dde0f794"
from django.http import HttpResponse




base_url = "http://api.openweathermap.org/data/2.5/weather?"


def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def update_weather(movie_request, request):
    movie_request = movie_request.replace(" ", "+")
    print(movie_request)
    complete_url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={movie_request}&language=fr-FR"
    print(complete_url)
    response = requests.get(complete_url)
    x = response.json()
    number_results = x ["total_results"]
    if number_results == 0:
        movie_title = "False_"
        poster_path = "False_"
        overview = "False_"
        movie_trailer_youtube = "False_"
        error_state = True
        #return HttpResponse("Erreur")
    else:

        print("Chargement de l'API...")
        main = x["results"]
        first = main[0]
        movie_id = first["id"]
        movie_type = first["media_type"]
        if movie_type == "movie":
            movie_title = first["original_title"]
        elif movie_type == "tv":
            movie_title = first["name"]
        #else:
        #    try:
        #        except ValueError:
        poster_path_ = first["poster_path"]
        poster_path = f"https://image.tmdb.org/t/p/w780/{poster_path_}"
        overview = first["overview"]
        
        
        movie_trailer_request = f"https://api.themoviedb.org/3/{movie_type}/{movie_id}/videos?api_key={api_key}"
        print(movie_trailer_request)
        response_trailer = requests.get(movie_trailer_request)
        x_trailer = response_trailer.json()
        try:
            main_trailer = x_trailer["results"]
            first_trailer = main_trailer[0]
            youtube_id_trailer = first_trailer["key"]
            movie_trailer_youtube = f"https://www.youtube.com/embed/{youtube_id_trailer}"
        except IndexError:
            main_trailer = "False_"
            first_trailer = "False_"
            youtube_id_trailer = "False_"
            movie_trailer_youtube = "False_"
            error_state = True
                        
        #print(movie_trailer_request)
        #print(movie_trailer_youtube)
        #movie_trailer_youtube = f"https://www.youtube.com/embed/Ozz8uxW733Q"
        #
        # = first[""]
        # = first[""]
        ######## change border radius css of the poster
        error_state = False
        if mobile(request):
            is_mobile = True
        else:
            is_mobile = False
        
        
            



    return error_state, movie_title, poster_path, overview, movie_trailer_youtube, is_mobile
        



# Create your views here.
def index(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        error_state, movie_title, poster_path, overview, movie_trailer_youtube, is_mobile = update_weather(search, request)
        if error_state == True:
            return HttpResponse("""<style>#error_text{font-size:50px;}</style><text id="error_text">Erreur</text>""")
        elif is_mobile == True:
            return HttpResponse("""<style>#error_text{font-size:50px;}</style><text id="error_text">Version mobile</text>""")
        
        elif is_mobile==False:
            return HttpResponse("""<style>#error_text{font-size:50px;}</style><text id="error_text">Version bureau</text>""")
        
        else:
            return render(request, "main.html", context={"movie_title": movie_title,"poster_path": poster_path,"overview": overview,"movie_trailer_youtube": movie_trailer_youtube,})
    ##return render(request, "blog-index.html", context={"date": date})
    return render(request, "index.html")
    #return HttpResponse("indexeeee")