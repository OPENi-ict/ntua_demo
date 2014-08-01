from django.contrib.gis import geoip
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.geoip import GeoIP
import pytz
import tzwhere
import arrow
import queryHandlers
import json
import recommenderParser

# Create your views here.
from django.views.decorators.http import require_GET
from tzwhere.tzwhere import tzwhere


def login(request):
    return render(request, "examples/login.html")

def logout(request):
    ## Put a check if user is logged in, before!
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/login")

def register(request):
    return None

@require_GET
def welcome(request):
    lat=23.7
    lng= 37.9
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    if ip and (ip!='127.0.0.1'):
        lat,lng=g.lat_lon(ip)
    city=g.city(ip)
    #now_utc = datetime.datetime.now()
    timezone=str(tzwhere().tzNameAt(lat, lng))
    utc2 = arrow.utcnow()
    local = utc2.to(timezone).format('YYYY-MM-DD HH:mm:ss')
    query="long=%s&lat=%s"%(lng,lat)
    #query="long=%s&lat=%s"%(lat,lng)
    places=queryHandlers.getRecommendations(query)
    print places
    return render_to_response('index.html', {"lat":lat, "long":lng, "city":city, "datetime":local, "places":places})

def widgets(request):
    return render(request, "widgets.html")

##Handle Session properties
def setContext(request):
    return render(request, "index.html")

def setSystem(request):
    return render(request, "index.html")

##Methods to connect with OPENi
def getPlaces(request):
    return render(request, "index.html")

def getPhotos(request):
    return render(request, "index.html")

def getEvents(request):
    return render(request, "index.html")