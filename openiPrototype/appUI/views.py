from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

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
    return render(request, "index.html")

def home(request):
    return render(request, "index.html")

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