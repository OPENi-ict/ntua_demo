# encoding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.geoip import GeoIP
import pytz
import tzwhere
import arrow, re
import ast
from appUI import apiURLs
import queryHandlers
from checkIfEnabled import checkIfEnabled
import json
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from tzwhere.tzwhere import tzwhere
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import condition
from appUI.forms import PersonForm
import foursquare
import FoursquareKeys
from models import Venue,VenueCategory,Checkin,Person, Rating
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
    #Get Places
    recommender=queryHandlers.RecommenderSECall(1)
    places=[]
    places=recommender.getPlaces(lat,lng) #call recommender
    #print "places: %s" %places
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
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    city=g.city(ip) #this method puts delay on the request, if not needed should be removed
    settings={}
    if request.method == 'POST':
        settings['educationSettings']=request.POST.get("educationSettings", "")
        settings['genderSettings']=request.POST.get("genderSettings", "")
        settings['ageSettings']=request.POST.get("ageSettings", "")
        settings['interestsSettings']=request.POST.get("interestsSettings", "")
        settings['daytimeSettings']=request.POST.get("daytimeSettings", "")
        lat=request.POST.get("latitudeTextbox", "")
        lng=request.POST.get("longitudeTextbox", "")
        userID=request.POST.get("userID", "")
        #print settings
    else:
        userID=request.user.id
        if ip and (ip!='127.0.0.1'):
            lat,lng=g.lat_lon(ip)
    timezone=str(tzwhere().tzNameAt(float(lat), float(lng)))
    utc2 = arrow.utcnow()
    local = utc2.to(timezone)

    if request.method=='POST':
        if checkIfEnabled(settings['daytimeSettings']):
            recommender=queryHandlers.RecommenderSECall(userID, checkIfEnabled(settings['educationSettings']),checkIfEnabled(settings['genderSettings']), checkIfEnabled(settings['ageSettings']),checkIfEnabled(settings['interestsSettings']),local)
        else:
            recommender=queryHandlers.RecommenderSECall(userID, checkIfEnabled(settings['educationSettings']),checkIfEnabled(settings['genderSettings']), checkIfEnabled(settings['ageSettings']),checkIfEnabled(settings['interestsSettings']) )
    else:
        recommender=queryHandlers.RecommenderSECall(userID, True,True, True,local)

    #places=[]
    places=recommender.getPlaces(lat,lng)
    args = {"lat":lat, "long":lng, "city":city, "datetime":local, "places":places, "user":request.user, "settings":settings, "searchUser":userID}
    args.update(csrf(request))
    return render_to_response('rec-places.html' , args)

def getRecProducts(request):
    # if not request.user.is_authenticated():
    #     # Do something for anonymous users.
    #     return HttpResponseRedirect("/login")
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    city=g.city(ip) #this method puts delay on the request, if not needed should be removed
    settings={}
    if ip and (ip!='127.0.0.1'):
            lat,lng=g.lat_lon(ip)
    if request.method == 'POST':
        settings['educationSettings']=request.POST.get("educationSettings", "")
        settings['genderSettings']=request.POST.get("genderSettings", "")
        settings['ageSettings']=request.POST.get("ageSettings", "")
        settings['interestsSettings']=request.POST.get("interestsSettings", "")
        settings['daytimeSettings']=request.POST.get("daytimeSettings", "")
        settings['categorySettings']=request.POST.get("categorySettings", "")
        userID=request.POST.get("userID", "")
        #print settings
    else:
        userID=request.user.id
    timezone=str(tzwhere().tzNameAt(float(lat), float(lng)))
    utc2 = arrow.utcnow()
    local = utc2.to(timezone)

    if request.method=='POST':
        if checkIfEnabled(settings['daytimeSettings']):
            recommender=queryHandlers.RecommenderSECall(userID, checkIfEnabled(settings['educationSettings']),checkIfEnabled(settings['genderSettings']), checkIfEnabled(settings['ageSettings']),checkIfEnabled(settings['interestsSettings']),local)
        else:
            recommender=queryHandlers.RecommenderSECall(userID, checkIfEnabled(settings['educationSettings']),checkIfEnabled(settings['genderSettings']), checkIfEnabled(settings['ageSettings']),checkIfEnabled(settings['interestsSettings']) )
    else:
        recommender=queryHandlers.RecommenderSECall(userID, True,True, True,local)

    products=recommender.getProducts()


    args = { "datetime":local, "products":products, "user":request.user, "settings":settings, "searchUser":userID, "productCategories":apiURLs.recommnederProductCategories}
    args.update(csrf(request))
    return render_to_response("rec-products.html",args)


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
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    statuses=queryHandlers.OpeniCall()
    statusesOfMe=statuses.getStatuses('me', 'facebook')
    args = { "statuses":statusesOfMe,  "user":request.user}
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
    photos=queryHandlers.OpeniCall()
    photosAround=photos.getPhotos(lat,lng,"instagram")
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

    if ip and (ip!='127.0.0.1'):
        lat,lng=g.lat_lon(ip)
    timezone=str(tzwhere().tzNameAt(float(lat), float(lng)))
    utc2 = arrow.utcnow()
    local = utc2.to(timezone).format('YYYY-MM-DD HH:mm:ss')
    photos=queryHandlers.OpeniCall()
    photosAround=photos.getPhotos(lat,lng,"instagram",'shopping, greece, athens')
    #print photosAround
    args = {"lat":lat, "long":lng, "city":city, "datetime":local, "photos":photosAround, "user":request.user}
    args.update(csrf(request))
    return render_to_response('rec-photos.html' , args)


def getPlacesAround(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    g = GeoIP()
    ip = request.META.get('REMOTE_ADDR', None)
    ip='147.102.1.1' #test IP for localhost requests. Remove on deployment
    city=g.city(ip) #this method puts delay on the request, if not needed should be remove
    places=[]
    places=queryHandlers.OpeniCall()
    placesAround=places.getPlaces(city["city"],'foursquare')
    #print placesAround
    args = { "places":placesAround, "user":request.user}
    args.update(csrf(request))
    return render_to_response('places.html' , args)


def getCheckins(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    return render(request, "checkins.html")


def getOrders(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    orders=queryHandlers.OpeniCall()
    ordersOfUser=orders.getOrders("open-i")
    i=0
    for order in ordersOfUser["objects"]: #Convert place from text to dictionary - bug needs to be fixed
        loc=order["From"]
        loc = loc.replace("u'", "'")
        loc= re.sub("[^\w]", " ",  loc).split()
        #loc=ast.literal_eval(loc)
        #print loc
        #shopsAround["objects"][i]["place"]={}
        ordersOfUser["objects"][i]["From"]={"object_type":"%s"%(loc[1]) , "id":"%s"%(loc[3]), "name":"%s"%(loc[5])}
        i+=1
    print ordersOfUser
    args = { "orders":ordersOfUser, "user":request.user}
    args.update(csrf(request))
    return render_to_response("orders.html",args)


def getShops(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/login")
    shops=queryHandlers.OpeniCall()
    shopsAround=shops.getShops("open-i")
    i=0
    for shop in shopsAround["objects"]: #Convert place from text to dictionary - bug needs to be fixed
        loc=shop["place"]
        loc = loc.replace("u'", "'")
        loc= re.sub("[^\w]", " ",  loc).split()
        #loc=ast.literal_eval(loc)
        #print loc
        #shopsAround["objects"][i]["place"]={}
        shopsAround["objects"][i]["place"]={"lat":"%s.%s"%(loc[1],loc[2]) , "lng":"%s.%s"%(loc[4],loc[5])}
        i+=1
    #print shopsAround
    args = { "shops":shopsAround, "user":request.user}
    args.update(csrf(request))
    return render_to_response("shops.html",args)


def authorizeAccounts(request):
    client = foursquare.Foursquare(client_id=FoursquareKeys.Foursquare_client_id, client_secret=FoursquareKeys.Foursquare_secret_key, redirect_uri='http://127.0.0.1:8000/authorize')
    if request.GET.get('code')==None:
        # Construct the client object
        # Build the authorization url for your app
        auth_uri = client.oauth.auth_url()
        print(auth_uri)
        args = {'4sqAuth':auth_uri}
        args.update(csrf(request))
        return render_to_response("syncAccounts.html", args)
    else:
        access_token = client.oauth.get_token(request.GET.get('code'))
        #client.set_access_token(access_token)
        #print('user: %s'%client.users.checkins)
        return HttpResponseRedirect("/authorizeSignup?access=%s"%access_token)



def authorizeSignup(request):
    if request.GET.get('access'):
        access = request.GET.get('access')
    else:
        access = request.POST.get('access')
    foursq=queryHandlers.FoursquareCall(access_token=access)
    #get user profiles
    user = foursq.getSelf()
    user_id= user['response']['user']['id']
    #get user checkins
    checkins=foursq.getCheckins(USER_ID=user_id)
    if not checkins:
        checkins=[]
    if request.method == "POST":
        person = PersonForm(request.POST)
        if person.is_valid():
            if not Person.objects.filter(fsq_user_id=user_id):
                personInstance = person.save()
                personInstance.setFsqID(user_id)
                personInstance.save()
            else:
                personInstance= Person.objects.get(fsq_user_id=user_id)
            # Do something.
            for checkin in checkins['response']['checkins'].get('items',None):
                #print checkin
                if not Checkin.objects.filter(service_id=checkin.get('id', None)):
                    #print 'Not stored the checkin'
                    #create venue
                    venue = Venue.objects.create(service_id = checkin['venue'].get('id',None) ,
                                                 name = u'%s'%checkin['venue'].get('name',None),
                                                 lat= checkin['venue']['location'].get('lat', None),
                                                 lng =checkin['venue']['location'].get('lng',None) ,
                                                 cc= u'%s'%checkin['venue']['location'].get('cc',None),
                                                 city=u'%s'%checkin['venue']['location'].get('city',None),
                                                 state= u'%s'%checkin['venue']['location'].get('state',None),
                                                 country= u'%s'%checkin['venue']['location'].get('country',None))
                    venue.save()
                    #create venue categories
                    for ctgry in checkin['venue'].get('categories',None):
                        category=VenueCategory.objects.create(service_id = ctgry.get('id',None) ,name = ctgry.get('name',None), venue=venue)
                    #create checkin
                    Checkin.objects.create (service_id = checkin.get('id',None),
                                            service = 'foursquare',
                                            createdAt = checkin.get('createdAt',None) ,
                                            createdBy  = personInstance,
                                            venue =venue).save()
                    #print 'created checkin /n'
            return render_to_response("thanks.html")
    else:
        person = PersonForm()
    args = { "personForm":person, "checkins":checkins, "access":access}
    args.update(csrf(request))
    return render_to_response("syncSignup.html", args)


def terms(request):
    return render_to_response("terms.html")


def rateProducts(request):

    if 'user' in request.session:
        user=request.session['user']
        #print user
    else:
        return HttpResponseRedirect("/train/")
    #if POST, initially store the latest score
    if request.method == "POST":
        #print request.POST.get('product_code')
        if request.POST.get('rate')!=None:
            rate=request.POST.get('rate')
        #store rate and continue
        newRate=Rating.objects.create(createdBy=Person.objects.get(pk=request.session['user']), rate=rate, product_id=request.POST.get('product_code'))
        newRate.save()

    #get a new product ID and navigate to that page
    if "products" in request.session:
        products = request.session["products"]
    else:
        products = []
    #print "products:%s"%products
    if len(products)==0:
        productsForRate=queryHandlers.ProductDB()
        products=productsForRate.getProducts(limit=4)
    #print products
    product=products.pop()
    if product["image"] is None:
        product=products.pop()
    if len(products)==0:
        productsForRate=queryHandlers.ProductDB()
        products=productsForRate.getProducts(limit=4)

    request.session["products"]=products
    # product_show={}
    # product_show["code"]=product["code"]
    # product_show["name"]=product["name"]
    # product_show["description"]= ""
    # product_show ["brand_name"]=product["brand_name"]
    # product_show ["brand_image"]=product["brand_image"]
    # product_show["image"]= product["image"]
    # product_show["category"]=product["gpc_name"]
    args = { "product":product}
    args.update(csrf(request))
    return render_to_response("rateProducts.html", args)



def train(request):
    if request.method == "POST":
        person = PersonForm(request.POST)
        if person.is_valid():
            personInstance = person.save()
            request.session['user'] = personInstance.id
            #get a product ID and navigate to that page
            return HttpResponseRedirect("/rate/new")
    else:
        person = PersonForm()
    args = { "personForm":person}
    args.update(csrf(request))
    return render_to_response("formForRating.html", args)


def recommenderAPI(request):
    return render_to_response("recommenderAPI.html")