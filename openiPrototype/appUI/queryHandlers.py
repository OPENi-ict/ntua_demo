__author__ = 'alvertisjo'
import urllib2,urllib
import apiURLs
import json
import requests
from requests.exceptions import ConnectionError,Timeout


class RecommenderSECall(object):
    def __init__(self,userID,education=False, gender=False,age=False, interests=False, timestamp=None):
        self.userID=userID
        self.timestamp=timestamp
        self.education=education
        self.gender=gender
        self.age=age
        self.interests=interests
    def setTimeStamp(self,timestamp):
        self.timestamp=timestamp
    def getPlaces(self,lat,lng):
        query="long=%s&lat=%s"%(lng,lat) #query properties for recommender    places=[]
        full_url="%s%s&id=%s"%(apiURLs.recommenderSE,query,self.userID)
        if self.education:
            full_url="%s&context=education"%full_url
        if self.gender:
            full_url="%s&context=gender"%full_url
        if self.age:
            full_url="%s&context=age"%full_url
        if self.interests:
            full_url="%s&context=interests"%full_url
        if self.timestamp is not None:
            full_url="%s&timestamp=%s"%(full_url,self.timestamp)
        try:
            response = requests.get(full_url)
            print "Recommender URL: %s" %full_url
            #print "got a respone with: %s" %response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            response = "No response"
            return json.dumps({"error":e.message})
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])

class OpeniCall(object):
    def __init__(self):
        self.app_name="OPENi"
        self.user="openihackathon"
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
        try:
            response = requests.get(full_url)
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return json.dumps({"error":e.message})
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])

    def getPlaces(self,city, cbs, radius=800, limit=12, user=None):
        if user is not None:
            self.user=user
        self.objectName='photo'
        self.cbs=cbs
        apps=[]
        app={}
        app["cbs"]=self.cbs
        app["app_name"]=self.app_name
        apps.append(app)
        self.data={}
        self.data["near"]=str(city) # not sure if needed to be sent as string or long
        self.data["radius"]=str(radius)
        self.data["categoryId"]='4bf58dd8d48988d116941735'
        self.data["limit"]='12'
        self.method="search_venues"
        ##example call: http://147.102.6.98:1988/v.04/photo/?user=romanos&apps=[{"cbs": "foursquare", "app_name": "OPENi"}]&method=search_venues&data={"near": "Athens", "limit": "12", "radius": "800", "categoryId": "4bf58dd8d48988d116941735"}
        query= "user=%s&apps=%s&method=%s&data=%s&format=json"%(self.user,str(apps),self.method, str(self.data))
        url = "%s%s/"%(apiURLs.platformAPI,self.objectName)
        full_url = url + '?' + query
        print full_url
        try:
            response = requests.get(full_url)
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])

    #http://localhost:1988/v.04/photo/?user=romanos.tsouroplis&apps=[{"cbs": "facebook", "app_name": "OPENi"}]&method=get_all_statuses_for_account&data={"account_id": "675350314"}
    def getStatuses(self,account_id, cbs=None, tags=None):
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
        query= "user=%s&apps=%s&method=%s&data=%s&format=json"%(self.username,str(apps),self.method, str(self.data))
        url = "%s%s/"%(apiURLs.platformAPI,self.objectName)
        full_url = url + '?' + query
        try:
            response = requests.get(full_url)
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])

    def getShops(self, cbs, user=None):
        self.objectName='shop'
        self.cbs=cbs
        full_url= "%s%s/?api_key=special-key&format=json"%(apiURLs.swaggerAPI,self.objectName)
        try:
            response = requests.get(full_url)
            #print response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])
    def getOrders(self, cbs, user=None):
        self.objectName='order'
        self.cbs=cbs
        full_url= "%s%s/?api_key=special-key&format=json"%(apiURLs.swaggerAPI,self.objectName)
        try:
            response = requests.get(full_url)
            print response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])

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
        full_url='%s%s'%(apiURLs.cloudletAPI,'cloudlets')
        print full_url
        print token
        headerCall={}
        headerCall["auth_token"]=  token
        print headerCall
        hdr={"auth_token": { "token": { "user": "dmccarthy" }, "signature": "cVnf/YsH/h+554tlAAh5CvyLr3Y9xrqAK4zxTA/C8PMDWcjcUZistg90H2HiCL/tAL3VZe/53VbJcrFZGyFZDw==" }}
        print(hdr)
        try:
            response = requests.get(full_url,headers=json.dumps(hdr),verify=False)
            print response.text
            print(response.json())
            return response
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            response = None
            return response
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])


        return None


class FoursquareCall(object):
    def __init__(self, access_token=None):
        self.version='20141016'
        self.access_token= access_token
        self.url='https://api.foursquare.com/v2/'

    def getSelf(self):
        full_url = "%susers/self?oauth_token=%s&v=%s"%(apiURLs.FoursquareURL, self.access_token,self.version)
        #print(full_url)
        try:
            response = requests.get(full_url, verify=False)
            #print response
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response.json()
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])
    def getCheckins(self,USER_ID=None):
        full_url = "%susers/%s/checkins?oauth_token=%s&v=%s&limit=250"%(apiURLs.FoursquareURL, USER_ID, self.access_token,self.version)
        print(full_url)
        try:
            response = requests.get(full_url, verify=False)
            #print response
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response.json()
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])
