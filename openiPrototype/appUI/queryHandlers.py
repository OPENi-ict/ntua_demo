__author__ = 'alvertisjo'
import urllib2,urllib
import apiURLs
import json
import requests
from requests.exceptions import ConnectionError,Timeout
from random import randrange
import json
from django.utils.dateformat import format as timeformat



class RecommenderSECall(object):
    def __init__(self,token, education=False, gender=False,age=False, interests=False, timestamp=None):
        self.token=token
        self.timestamp=timestamp
        self.education=education
        self.gender=gender
        self.age=age
        self.interests=interests

    def setTimeStamp(self,timestamp):
        self.timestamp=timestamp
    def getPlaces(self,lat,lng,rad=3000):
        query="places?long=%s&lat=%s&rad=%s"%(lng,lat,rad) ##Add location properties
        full_url="%s%s"%(apiURLs.recommenderSE,query)#self.userID)  ##Add user ID
        ##Add contextual properties
        context=[]
        if self.education:
            context.append("education")
        if self.gender:
            context.append("gender")
        if self.age:
            context.append("age")
        if self.interests:
            context.append("interests")
        if not context:
            full_url="%s&context=all"%full_url
        else:
            full_url="%s&context="%full_url
            for contextProperty in context:
                full_url="%s%s,"%(full_url,contextProperty)
            if full_url.endswith(','):
                full_url = full_url[:-1]
        ##END: Add contextual properties

        if self.timestamp is not None:
            full_url="%s&timestamp=%s"%(full_url,timeformat(self.timestamp,u'U'))
        try:
            header={"Authorization":self.token}
            response = requests.get(full_url,headers=header)
            print "Recommender URL: %s" %full_url
            #print "got a respone with: %s" %response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            response = "No response"
            return json.dumps({"error":"connection error"})
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except requests.exceptions.RequestException as e:
            if self.request.retries >= self.max_retries:
                print "max retries: %s" %e
                return json.dumps({"error":"max retries"})
            raise self.retry(exc=e)
        except:
            return json.dumps([])

    def getProducts(self, category=None, method=None):
        extraString=""
        if str(category).lower()!='all':
            extraString="&category=%s"%category
        ##Add contextual properties
        full_url="%sproducts/?currency=euro&shop=12&sortParam=%s%s"%(apiURLs.recommenderSE,method,extraString)  ##Add user ID
        context=[]
        if self.education:
            context.append("education")
        if self.gender:
            context.append("gender")
        if self.age:
            context.append("age")
        if self.interests:
            context.append("interests")
        if not context:
            full_url="%s&context=all"%full_url
        else:
            full_url="%s&context="%full_url
            for contextProperty in context:
                full_url="%s%s,"%(full_url,contextProperty)
            if full_url.endswith(','):
                full_url = full_url[:-1]
        ##END: Add contextual properties

        if self.timestamp is not None:
            full_url="%s&timestamp=%s"%(full_url,self.timestamp)

        try:
            header={"Authorization":self.token}
            response = requests.get(full_url,headers=header)
            print "Recommender URL: %s" %full_url
            print "got a respone with: %s" %response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            #print "error: %s" %e
            response = "No response"
            return json.dumps({"error":"connection error"})
        except Timeout as t:    # This is the correct syntax
            #print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])
    def getProductCategories(self):
        full_url="%sproducts/categories/" %apiURLs.recommenderSE
        try:
            response = requests.get(full_url)
            print "Recommender URL: %s" %full_url
            #print "got a respone with: %s" %response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            #print "error: %s" %e
            response = "No response"
            return json.dumps({"error":"connection error"})
        except Timeout as t:    # This is the correct syntax
            #print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])
    def getApplications(self):
        pass

class OpeniCall(object):
    def __init__(self,token=None):
        self.app_name="OPENi"
        self.user="openihackathon"
        self.tags=''
        self.token=token
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
            return json.dumps({"error":"connection error"})
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            response = "No response"
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])

    def getPlaces(self,city, cbs, radius=3000, limit=20, user=None):
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
    def getContext(self, objectID=None):
        self.objectName='Context'
        self.cbs='openi'
        full_url= "%s"%(apiURLs.searchAPIPath)
        try:
            header={"Authorization":self.token}
            response = requests.get(full_url,headers=header)
            #print response.text
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except requests.exceptions.RequestException as e:
            if self.request.retries >= self.max_retries:
                print "max retries: %s" %e
                return json.dumps({"error":"connection error"})
            raise self.retry(exc=e)
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
        #print(hdr)
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
        ##print(full_url)
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
    def getPlacesAround(self, lat,lng,radius=3000):
        full_url = "%svenues/search?oauth_token=%s&v=%s&ll=%s,%s&limit=50"%(apiURLs.FoursquareURL, self.access_token,self.version,lat,lng)
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


class ProductDB(object):
    def __init__(self, access_token=None):
        self.access_token= access_token
        self.productsIDs=["70000000","68000000","77000000","54000000",
                          #"53000000",
                          "83000000","47000000","67000000","66000000","65000000","58000000","78000000","50000000","63000000","51000000","72000000","75000000","73000000","81000000","88000000","61000000","64000000","10000000","79000000","85000000","71000000","62000000","84000000","80000000","82000000","86000000"]
    def getRandomCategory (self):
        categories=self.productsIDs
        # with open('product-categories.json') as f:
        #     for line in f:
        #         data.append(json.loads(line))
        return categories[randrange(len(categories))]
    def getProducts(self, limit=3):
        #full_url = "%s?limit=%s&category=%s"%(apiURLs.productsDBurl, limit, self.getRandomCategory())
        full_url = "%s?limit=%s"%(apiURLs.productsDBurl, limit)
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


class OPENiOAuth(object):
    def __init__(self):
        self.access_token= None
        self.session= None
        self.created= None
        self.status_code=None
    def getAccessToken(self):
        return self.access_token
    def getSessionToken(self):
        return self.session
    def getSession(self, username, password):
        full_url = "%ssessions"%(apiURLs.demo2APIoAuth)
        print(full_url)
        try:
            #data={"username":username,"password":password, "scope":""}
            data='{"username":"%s","password":"%s", "scope":""}'%(username,password)
            response = requests.post(full_url, data, verify=False)
            #print response
            self.status_code=response.status_code
            self.session=response.json()["session"]
            print self.session
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            self.access_token=None
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            self.access_token=None
        except:
            self.access_token=None
    def authorize(self, username, password):
        self.getSession(username,password)
        full_url = "%sauthorizations"%(apiURLs.demo2APIoAuth)
        print(full_url)
        try:
            data={"session":self.session,"client_id":username}
            response = requests.post(full_url, data, verify=False)
            #print response
            self.status_code=response.status_code
            self.access_token=response.json()["token"]
            return response.json()
        except ConnectionError as e:    # This is the correct syntax
            print "error: %s" %e
            return response.json()
        except Timeout as t:    # This is the correct syntax
            print "Timeout error: %s" %t
            return json.dumps({"error":t.message})
        except:
            return json.dumps([])