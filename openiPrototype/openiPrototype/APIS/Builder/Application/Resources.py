__author__ = 'mpetyx'

from tastypie.resources import ModelResource
from OPENiapp.APIS.OpeniGenericResource import GenericResource
from OPENiapp.APIS.OPENiAuthorization import Authorization
from OPENiapp.APIS.OPENiAuthentication import Authentication

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken


class CBSResource(ModelResource):
    class Meta:
        queryset = SocialApp.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'socialapp'
        authentication = Authentication()
        authorization = Authorization()
        # filtering = {
        #     'slug': ALL,
        #     'user': ALL_WITH_RELATIONS,
        #     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        # }

class SocialAccountResource(ModelResource):
    class Meta:
        queryset = SocialAccount.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'SocialAccount'
        authentication = Authentication()
        authorization = Authorization()
        # filtering = {
        #     'slug': ALL,
        #     'user': ALL_WITH_RELATIONS,
        #     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        # }

class SocialTokenResource(ModelResource):
    class Meta:
        queryset = SocialToken.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'SocialToken'
        authentication = Authentication()
        authorization = Authorization()
        # filtering = {
        #     'slug': ALL,
        #     'user': ALL_WITH_RELATIONS,
        #     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        # }