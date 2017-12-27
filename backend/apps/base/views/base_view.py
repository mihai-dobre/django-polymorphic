import math

# rest framework related imports
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework_xml.parsers import XMLParser
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.exceptions import AuthenticationFailed
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from django_auth_ldap.backend import LDAPBackend


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


class PaginationMixIn():
    def paginate(self, objects):
        page_size = int(self.request.query_params.get('page_size', settings.DEFAULT_PAGE_SIZE))
        if page_size != -1:
            total_objects = len(objects)
            paginator = Paginator(objects, page_size)
            page = int(self.request.query_params.get('page', 1))
            try:
                objects = paginator.page(page)
            except PageNotAnInteger:
                objects = paginator.page(1)
            except EmptyPage:
                objects = paginator.page(paginator.num_pages)

            response = {}
            response['objects'] = objects.object_list
            response['page_number'] = page
            response['total_pages'] = int(math.ceil(total_objects / float(page_size)))
            response['page_size'] = page_size
        else:
            response = {'objects': objects}
        return response


class ApiBaseView(APIView):
    authentication_classes = (BasicAuthentication, OAuth2Authentication, SessionAuthentication, LDAPBackend)
    # add permission class to check the priority(if a service is available for a certain user) and the maximum amount
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, XMLParser)
    renderer_classes = (JSONRenderer, XMLRenderer)
