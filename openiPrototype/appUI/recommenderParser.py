class Recommendations(object):

    def __init__(self):
        """
        : attribute categories : array
        : attribute name : string
        : attribute location : Location
        : attribute url : string
        """
        self.categories = None
        self.name = None
        self.location = None
        self.url = None


class Location(object):

    def __init__(self):
        """
        : attribute address : string
        : attribute city : string
        : attribute country : string
        : attribute formatted_address : array
        : attribute cross_street : string
        : attribute distance : float
        : attribute postal_code : string
        : attribute lat : float
        : attribute lng : float
        : attribute cc : string
        : attribute state : string
        """
        self.address = None
        self.city = None
        self.country = None
        self.formatted_address = None
        self.cross_street = None
        self.distance = None
        self.postal_code = None
        self.lat = None
        self.lng = None
        self.cc = None
        self.state = None


class BaseClass(object):

    def __init__(self):
        """
        : attribute recommendations : array
        """
        self.recommendations = None
