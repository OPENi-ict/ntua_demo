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
from django.contrib.auth.models import User
from tzwhere.tzwhere import tzwhere
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import condition


latitude=23.7
longitude=37.9

def signout(request):
    ## Put a check if user is logged in, before!
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/login")

def welcome(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
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
    args = {"lat":lat, "long":lng, "city":city, "datetime":local, "places":places, "settings":settings, "photos":photosAround, "user":request.user}
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
def getRecPlaces(request):
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    if ip and (ip!='127.0.0.1'):
            lat,lng=g.lat_lon(ip)
    query="long=%s&lat=%s"%(lng,lat) #query properties for recommender    places=[]
    places=[]
    places=queryHandlers.getRecommendations(query) #call recommender
    args = { "places":places, "user":request.user}
    args.update(csrf(request))
    return render_to_response('places.html' , args)

def getPhotos(request):
    return render(request, "index.html")

def getEvents(request):
    return render(request, "index.html")

@csrf_protect
def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/") # Redirect after POST

    if request.method == 'POST': # If the form has been submitted...
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                #set user on session property to read it from results
            else:
                return HttpResponseRedirect("/login") # Redirect after POST
        else:
            # the authentication system was unable to verify the username and password
            return HttpResponseRedirect("/login") # Redirect after POST
        #Check authenticated
        return HttpResponseRedirect("/") # Redirect after POST
    else:
        return render(request, "login.html")

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/") # Redirect after POST
    else:
        if request.method == 'POST': # If the form has been submitted...
            username=request.POST.get("username","")
            email=request.POST.get("email","")
            password=request.POST.get("password","")
            password2=request.POST.get("password2","")
            if str(username).isspace() or str(email).isspace() or str(password).isspace(): #strings with gaps
                return render(request, "register.html", {"message": 'Please fill in all the fields'})
            elif not str(username) or not str(email) or not str(password) or not str(password2): #empty strings
                return render(request, "register.html", {"message": 'Please fill in all the fields'})
            elif User.objects.filter(username=(str(username).lower())): #user exists
                return render(request, "register.html", {"message": 'Choose another username'})
            elif User.objects.filter(username=(str(email).lower())): # email exists
                return render(request, "register.html", {"message": 'This email is already in use'})
            elif str(password)!= str(password2): #not same password
                return render(request, "register.html", {"message": 'Wrong password verification'})
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
            return HttpResponseRedirect("/")
        return render(request, "register.html")


def getStatuses(request):
    statuses=queryHandlers.OpeniCall()
    statuses=statuses.getStatuses('me','iosif', 'facebook')
    args = { "statuses":statuses,  "user":request.user}
    args.update(csrf(request))
    return render_to_response('timeline.html' , args)


def getPicAround(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    lat=23.7
    lng= 37.9
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    if ip and (ip!='127.0.0.1'):
            lat,lng=g.lat_lon(ip)

    #print "cloudletid:%s"%queryHandlers.CloudletCall()

    photos=queryHandlers.OpeniCall()
    photosAround=photos.getPhotos(lat,lng,"instagram",)
    args = {"lat":lat, "long":lng, "photos":photosAround, "user":request.user}
    args.update(csrf(request))

    return render_to_response('photosAround.html' , args)


def getRecPhotos(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
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
    photos=queryHandlers.OpeniCall()
    photosAround=photos.getPhotos(lat,lng,"instagram",'shopping, greece, athens')
    args = {"lat":lat, "long":lng, "city":city, "datetime":local, "settings":settings, "photos":photosAround, "user":request.user}
    args.update(csrf(request))
    return render_to_response('rec-photos.html' , args)