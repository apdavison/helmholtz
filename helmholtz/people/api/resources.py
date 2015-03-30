# people/api.py

from django.contrib.auth.models import User
from django.conf.urls import url
from django.contrib.contenttypes.models import ContentType

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.core.api.authorization import GuardianAuthorization
from helmholtz.core.api.serialization import HelmholtzSerializer

from helmholtz.people.models import Organization
from helmholtz.people.models import Researcher
from helmholtz.people.models import Position
from helmholtz.people.models import Supplier

# Additionals models
from helmholtz.units.models import Unit
from helmholtz.measurements.models import Parameter
from helmholtz.measurements.models import Measurement


# Resources
class OrganizationResource( ModelResource ) :
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'name': ALL,
            'diminutive': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class UserResource( ModelResource ) :
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['id','password', 'is_superuser', 'is_staff', 'is_active']
        filtering = {
            'username': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        serializer = HelmholtzSerializer()


class ResearcherResource( ModelResource ) :
    #user = fields.ForeignKey( UserResource, 'user' )
    user = fields.ForeignKey( UserResource, attribute='user', full=True )
    
    # output measurement in addition to normal fields
    #def dehydrate( self, bundle ) :
    #    # get the content_type id for the current resource
    #    ctype = ContentType.objects.get( model=self._meta.resource_name )
    #    # get the measurements for the current resource object
    #    related_to_model = Measurement.objects.filter( content_type=ctype, object_id=bundle.obj.pk )
    #    #if len( related_to_model ) : if we want that measurement is absent from unmeasured items
    #    bundle.data['measurements'] = related_to_model # always present even if empty
    #    return bundle

    class Meta:
        queryset = Researcher.objects.all()
        resource_name = 'researcher'
        excludes = ['id']
        filtering = {
            'user' : ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()
        authorization = GuardianAuthorization()
        serializer = HelmholtzSerializer()

class PositionResource( ModelResource ) :
    researcher = fields.ForeignKey( ResearcherResource, 'researcher' )
    structure = fields.ForeignKey( OrganizationResource, 'structure' )

    class Meta:
        queryset = Position.objects.all()
        resource_name = 'position'
        excludes = ['id']
        filtering = {
            'type': ALL,
            'researcher': ALL_WITH_RELATIONS,
            'structure': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SupplierResource( ModelResource ) :
    class Meta:
        queryset = Supplier.objects.all()
        resource_name = 'supplier'
        excludes = ['id']
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
