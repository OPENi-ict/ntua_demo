__author__ = 'mpetyx'

from .models import OpeniPhoto

from OPENiapp.Providers.Facebook.connector import provider as FBprovider
from OPENiapp.Providers.Twitter.connector import provider as TWprovider
from allauth.socialaccount.models import SocialToken

from OPENiapp.APIS.OpeniGenericResource import GenericResource
from OPENiapp.APIS.OPENiAuthorization import Authorization
from OPENiapp.APIS.OPENiAuthentication import Authentication

from tastypie.serializers import Serializer
from tastypie import fields
from OPENiapp.APIS.Context.Resources import ContextResource

class PhotoResource(GenericResource):

    # journey = fields.ForeignKey(WorkJourneyResource, 'work_journey', null=True, blank=True)
    class Meta:
        queryset = OpeniPhoto.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'photo'
        authentication = Authentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])

        # filtering = {
        #     'slug': ALL,
        #     'user': ALL_WITH_RELATIONS,
        #     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        # }
        
    def make_fb_connection(self, user):
        """ Use facepy to make a Graph API call """
        return FBprovider(
            access_token=SocialToken.objects.filter(account__user=user.id, account__provider='facebook'))

    def obj_create(self, bundle, request=None, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)
        self.save(bundle)

        #   Post to FB
        json_return_fb_photo_post = None
        if ("facebook" in bundle.data) and (bundle.data["facebook"] == 'on'):
            fbconnector = self.make_fb_connection(bundle.request.user)
            json_return_fb_photo_post = fbconnector.post_photo(bundle.data["path"])
            bundle.data["facebook_result"] = json_return_fb_photo_post
            
        #   Post to Twitter
        json_return_tw_photo_post = None
        if ("twitter" in bundle.data) and (bundle.data["twitter"] == 'on'):
            app_name = "Twitter"
            twconnector = TWprovider(app_name, bundle.request.user)
            json_return_tw_photo_post = twconnector.post_photo(bundle.data['path'])
            bundle.data["twitter_result"] = json_return_tw_photo_post

        return bundle