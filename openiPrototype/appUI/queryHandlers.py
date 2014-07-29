__author__ = 'alvertisjo'
import urllib2,urllib
import apiURLs
import json


def getRecommendations(query):
    response = urllib2.urlopen(
        "%s%s"%(apiURLs.recommenderSE,query)
    )
    response = response.read()
    response = json.loads(response)
    return response
