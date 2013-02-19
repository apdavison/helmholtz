# people/api.py

from django.contrib.auth.models import User
from django.conf.urls.defaults import url

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
# measurement
from tastypie.utils import trailing_slash
from tastypie.http import HttpBadRequest
from tastypie.http import HttpForbidden
from tastypie.http import HttpCreated

from helmholtz.people.models import ScientificStructure
from helmholtz.people.models import Researcher
from helmholtz.people.models import Position
from helmholtz.people.models import Supplier

# Additionals models
from django.contrib.contenttypes.models import ContentType
from helmholtz.units.models import Unit
from helmholtz.measurements.models import Parameter
from helmholtz.measurements.models import Measurement


# Resources
class ScientificStructureResource( ModelResource ) :
    class Meta:
        queryset = ScientificStructure.objects.all()
        resource_name = 'scientificstructure' # optional, if not present it will be generated from classname
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
        excludes = ['password', 'is_superuser', 'is_staff', 'is_active']
        filtering = {
            'username': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ResearcherResource( ModelResource ) :
    user = fields.ForeignKey( UserResource, 'user' )
    
    # to have measurements and annotations in the url
    def prepend_urls( self ) :
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/measurement/*" % self._meta.resource_name, self.wrap_view('set_measurements'), name="api_set_measurements"),
            #url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/measurement/*" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def set_measurements( self, request, **kwargs ) :
        self.method_check( request, allowed=['post'] )
        self.is_authenticated( request )
        # create resource to have the bundle
        pk = int(kwargs['pk'])
        #rr = ResearcherResource()
        #researcher = rr.obj_get(  
        # data values
        # get resources
        #parameter = Parameter.objects.get( label=label )
        #unit = Unit.objects.get( symbol=symbol )
        #ctype = ContentType.objects.get( model=self._meta.resource_name )
        #measurement = Measurement( parameter=parameter, unit=unit, content_type=ctype, object_id=bundle.obj.pk, float_value=value )
        response = HttpForbidden
        if pk == 2 :
            response = HttpCreated
        else:
            response = HttpBadRequest
        return self.create_response( request, [], response_class=response )

    # output measurement in addition to normal fields
    def dehydrate( self, bundle ) :
        # get the content_type id for the current resource
        ctype = ContentType.objects.get( model=self._meta.resource_name )
        # get the measurements for the current resource object
        related_to_model = Measurement.objects.filter( content_type=ctype, object_id=bundle.obj.pk )
        #if len( related_to_model ) : if we want that measurement is absent from unmeasured items
        bundle.data['measurements'] = related_to_model # always present even if empty
        return bundle

    class Meta:
        queryset = Researcher.objects.all()
        resource_name = 'researcher'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        filtering = {
            'id' : ALL,
            'user' : ALL_WITH_RELATIONS,
        }


class PositionResource( ModelResource ) :
    researcher = fields.ForeignKey( ResearcherResource, 'researcher' )
    structure = fields.ForeignKey( ScientificStructureResource, 'structure' )

    class Meta:
        queryset = Position.objects.all()
        resource_name = 'position'
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
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
