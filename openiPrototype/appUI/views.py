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
from django.core.context_processors import csrf
from django.template import RequestContext

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

def welcome(request):
    lat=23.7
    lng= 37.9
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    city=g.city(ip) #this method puts delay on the request, if not needed should be removed
    #print places
    settings={}
    if request.method == 'POST':
        settings['locationSettings']=request.POST.get("locationSettings", "")
        settings['daytimeSettings']=request.POST.get("daytimeSettings", "")
        settings['profileSettings']=request.POST.get("profileSettings", "")
        settings['friendsSettings']=request.POST.get("friendsSettings", "")
        settings['activitySettings']=request.POST.get("activitySettings", "")
        settings['moodSettings']=request.POST.get("moodSettings", "")
        settings['weekdaySettings']=request.POST.get("weekdaySettings", "")
        settings['interestsSettings']=request.POST.get("interestsSettings", "")
        lat=request.POST.get("latitudeTextbox", "")
        lng=request.POST.get("longitudeTextbox", "")
        #print settings
    else:
        if ip and (ip!='127.0.0.1'):
            lat,lng=g.lat_lon(ip)
    timezone=str(tzwhere().tzNameAt(float(lat), float(lng)))
    utc2 = arrow.utcnow()
    local = utc2.to(timezone).format('YYYY-MM-DD HH:mm:ss')
    query="long=%s&lat=%s"%(lng,lat) #query properties for recommender
    places=[]
    places=queryHandlers.getRecommendations(query) #call recommender

    photos=queryHandlers.OpeniCall()
    photosAround=photos.getPhotos(lat,lng,"instagram")
    args = {"lat":lat, "long":lng, "city":city, "datetime":local, "places":places, "settings":settings, "photos":photosAround}
    args.update(csrf(request))
    return render_to_response('index.html' , args)

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