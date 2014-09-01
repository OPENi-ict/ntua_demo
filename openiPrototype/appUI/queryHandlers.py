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


class OpeniCall(object):
    def __init__(self):
        self.app_name="OPENi"
        self.user="tsourom"
    def getPhotos(self,lat, lng, cbs, tags=None):
        self.objectName='photo'
        self.cbs=cbs
        #self.method='filter_tags_photos'
        self.method="search_media"
        #self.cbs='instagram'
        apps=[]
        app={}
        app["cbs"]=self.cbs
        app["app_name"]=self.app_name
        apps.append(app)
        tags=[]
        tags.append(tags)
        self.data={}
        self.data["lat"]=str(lat) # not sure if needed to be sent as string or long
        self.data["lng"]=str(lng)
        ##if tags:
        ##    self.data['tags']=tags

        ##example call: ### http://147.102.6.98t:1988/v.04/photo/?user=tsourom&apps=[{"cbs": "instagram", "app_name": "OPENi"}]&method=filter_tags_photos&data={"lat": "37.9667", "lng": "23.7167", "tags": ["athens"]}
        query= "user=%s&apps=%s&method=%s&data=%s&format=json"%(self.user,str(apps),self.method, str(self.data))
        url = "%s%s/"%(apiURLs.platformAPI,self.objectName)
        full_url = url + '?' + query
        response=urllib.urlopen(full_url)
        response=response.read()
        response = json.loads(response)
        return response