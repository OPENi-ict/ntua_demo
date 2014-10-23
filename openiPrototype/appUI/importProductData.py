__author__ = 'alvertisjo'

from django.core.serializers import json
import requests
from requests.packages.urllib3 import Timeout
from requests.packages.urllib3.exceptions import ConnectionError

class OpenProductData(object):

    def getData(self):
        # rowStep=100
        # currentPage=0
        # #####documentation: http://pod.opendatasoft.com/api/doc/#doc-datasets-search
        # full_url='http://pod.opendatasoft.com/api/records/1.0/search' #http://pod.opendatasoft.com/api/records/1.0/search?dataset=pod_gtin&rows=10&start=11&facet=gpc_s_nm&facet=brand_nm&facet=owner_nm&facet=gln_nm&facet=prefix_nm
        # dataset='pod_gtin'
        # #print(full_url)
        # try:
        #     response = requests.get(full_url, verify=False)
        #     #print response
        #     return response.json()
        # except ConnectionError as e:    # This is the correct syntax
        #     print "error: %s" %e
        #     return response.json()
        # except Timeout as t:    # This is the correct syntax
        #     print "Timeout error: %s" %t
        #     return json.dumps({"error":t.message})
        # except:
        #     return json.dumps([])
        pass
    def readDataFromFile(self):
        pass
    def storeToGraph(self,data):
        # POST http://localhost:7474/db/data/transaction/commit
        # Accept: application/json; charset=UTF-8
        # Content-Type: application/json
        url= 'http://snf-561492.vm.okeanos.grnet.gr:7474/'
        # {
        #   "statements" : [ {
        #     "statement" : "CREATE (n) RETURN id(n)"
        #   } ]
        # }
        pass