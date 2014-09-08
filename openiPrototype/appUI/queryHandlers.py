__author__ = 'alvertisjo'
import urllib2,urllib
import apiURLs
import json
import requests
from requests.exceptions import ConnectionError


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
        self.tags=''
    def getPhotos(self,lat, lng, cbs, tags=None):
        self.objectName='photo'
        self.cbs=cbs
        apps=[]
        app={}
        app["cbs"]=self.cbs
        app["app_name"]=self.app_name
        apps.append(app)
        self.data={}
        self.data["lat"]=str(lat) # not sure if needed to be sent as string or long
        self.data["lng"]=str(lng)
        print tags
        if tags!=None:
            searchtags=[]
            for tag in tags.split(','):
                searchtags.append(str(tag).replace(" ", ""))
            #searchtags.append(str(tags))
            self.method="filter_tags_photos"
            #self.tags="&tags=[\"%s\"]"%tags
            self.data["tags"]=searchtags
        else:
            self.method="search_media"
        ##example call: ### http://147.102.6.98t:1988/v.04/photo/?user=tsourom&apps=[{"cbs": "instagram", "app_name": "OPENi"}]&method=filter_tags_photos&data={"lat": "37.9667", "lng": "23.7167", "tags": ["athens"]}
        ##example call with tags: http://147.102.6.98t:1988/v.04/photo/?user=tsourom&apps=[{"cbs": "instagram", "app_name": "OPENi"}]&method=filter_tags_photos&data={"lat": "37.9667", "lng": "23.7167", "tags": ["athens"]}
        query= "user=%s&apps=%s&method=%s&data=%s&format=json"%(self.user,str(apps),self.method, str(self.data))
        url = "%s%s/"%(apiURLs.platformAPI,self.objectName)
        full_url = url + '?' + query
        #print full_url
        # response=urllib.urlopen(full_url)
        # response=response.read()
        # response = json.loads(response)
        try:
            response = requests.get(full_url)
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            response = "No response"
            return response





    #http://localhost:1988/v.04/photo/?user=romanos.tsouroplis&apps=[{"cbs": "facebook", "app_name": "OPENi"}]&method=get_all_statuses_for_account&data={"account_id": "675350314"}
    def getStatuses(self,account_id, username, cbs, tags=None):
        self.objectName='photo'
        self.cbs=cbs
        #self.method='filter_tags_photos'
        self.method="get_all_statuses_for_account"
        #self.cbs='instagram'
        apps=[]
        app={}
        app["cbs"]=self.cbs
        app["app_name"]=self.app_name
        apps.append(app)
        tags=[]
        tags.append(tags)
        self.data={}
        self.data["account_id"]=str(account_id) # not sure if needed to be sent as string or long
        ##if tags:
        ##    self.data['tags']=tags
        ##example call: ### http://147.102.6.98t:1988/v.04/photo/?user=tsourom&apps=[{"cbs": "instagram", "app_name": "OPENi"}]&method=filter_tags_photos&data={"lat": "37.9667", "lng": "23.7167", "tags": ["athens"]}
        query= "user=%s&apps=%s&method=%s&data=%s&format=json"%(username,str(apps),self.method, str(self.data))
        url = "%s%s/"%(apiURLs.platformAPI,self.objectName)
        full_url = url + '?' + query
        response=urllib.urlopen(full_url)
        response=response.read()
        response = json.loads(response)
        return response


class CloudletCall(object):
    def __init__(self,signature=None,user=None):
        self.signature="Ko49aYdt2+1YHtaUSNbfAXfp6LYe2svOW7h5mA+WNLYZH+hFCykwQ1a+1Ig9i3DM5g1PBcsHdig3NIToyKANDQ=="
        self.user="Alexis"
        self.id=''
        token={}
        user_tmp={}
        user_tmp['user']=self.user
        #{ "token": { "user": "dmccarthy" }, "signature": "cVnf/YsH/h+554tlAAh5CvyLr3Y9xrqAK4zxTA/C8PMDWcjcUZistg90H2HiCL/tAL3VZe/53VbJcrFZGyFZDw==" }
        token['token']=user_tmp
        token['signature']=self.signature
        url='%s%s'%(apiURLs.cloudletAPI,'cloudlets')
        print url
        print token
        header = {"auth_token": {"token": { "token": { "user": "dmccarthy" }, "signature": "cVnf/YsH/h+554tlAAh5CvyLr3Y9xrqAK4zxTA/C8PMDWcjcUZistg90H2HiCL/tAL3VZe/53VbJcrFZGyFZDw==" }},"Connection":"close"}
        try:
           r = requests.get(url)
           print r
        except ConnectionError as e:    # This is the correct syntax
           print "error: %s" %e
           r = "No response"

        # response=urllib.urlopen(url)
        # response=response.read()
        # response = json.loads(response)
        # self.id=response.id
        return None

