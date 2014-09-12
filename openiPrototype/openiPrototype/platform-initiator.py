# -*- coding: ascii -*-

__author__ = 'alvertisjo'
from APIS.Products_and_Services.Product.models import OpeniProduct
from APIS.Products_and_Services.Shop.models import OpeniShop
import random,json

class initiate(object):
    def __init__(self):
        self.generateAll()
    def generateShops (self,number):
        for i in range (1,number):
            newShop=OpeniShop ()
            foo=['a','b','c']
            newShop.currency= str(random.choice(foo))
            newShop.service='openi'
            print(json.dumps(newShop))

    def generateProducts (self,number):
        for i in range (1,number):
            newProduct=OpeniProduct()
            newProduct.amount=str(random.randint(1,100))
            foo=['a','b','c']
            newProduct.currency=str(random.choice(foo))
            newProduct.code=str(random.randint(1000000,99999999))
            newProduct.object_type='product'
            newProduct.service='openi'
            newProduct.price= str(random.randint(10,1500))
            #newProduct.From=
            print(json.dumps(newProduct))

    def generateAll (self):
        self.generateShops(10)
        self.generateProducts(100)

initiate()