__author__ = 'mpetyx'


from .models import OpeniBadge

from OPENiapp.APIS.OpeniGenericResource import GenericResource
from OPENiapp.APIS.OPENiAuthorization import Authorization
from OPENiapp.APIS.OPENiAuthentication import Authentication


class BadgeResource(GenericResource):
    class Meta:
        queryset = OpeniBadge.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'badge'
        authentication = Authentication()
        authorization = Authorization()
        # filtering = {
        #     'slug': ALL,
        #     'user': ALL_WITH_RELATIONS,
        #     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        # }


        extra_actions = [

            {
                "name": "comments",
                "http_method": "GET",
                "resource_type": "list",
                "description": "comments from CBS",
                "fields": {
                    "cbs": {
                        "type": "string",
                        "required": True,
                        "description": "list of selected CBS"
                    }
                }
            },

            {
                "name": "likes",
                "http_method": "GET",
                "resource_type": "list",
                "description": "likes from CBS",
                "fields": {
                    "cbs": {
                        "type": "string",
                        "required": True,
                        "description": "list of selected CBS"
                    }
                }
            },

            {
                "name": "dislikes",
                "http_method": "GET",
                "resource_type": "list",
                "description": "dislikes from CBS",
                "fields": {
                    "cbs": {
                        "type": "string",
                        "required": True,
                        "description": "list of selected CBS"
                    }
                }
            }
        ]