# device/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.devices.models import Item
from helmholtz.devices.models import Type
from helmholtz.devices.models import ItemProperties
from helmholtz.devices.models import RecordingPoint
from helmholtz.devices.models import SubSystem
from helmholtz.devices.models import Setup

# Allowed resources
from helmholtz.people.api.resources import OrganizationResource # example, add the others here
from helmholtz.people.api.resources import SupplierResource
from helmholtz.locations.api.resources import PositionResource
from helmholtz.chemistry.api.resources import SolutionResource
from helmholtz.chemistry.api.resources import ProductResource


# Resources
class TypeResource( ModelResource ) :
    class Meta:
        queryset = Type.objects.all()
        resource_name = 'type' # optional, if not present it will be generated from classname
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ItemResource( ModelResource ) :
    type = fields.ForeignKey( TypeResource, 'type' )
    manufacturer = fields.ForeignKey( SupplierResource, 'manufacturer', null=True )
    
    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle
    
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'model': ALL,
            'version': ALL,
            'serial_or_id': ALL,
            'manufacturer': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

 
class ItemPropertiesResource( ModelResource ) :
    item = fields.ForeignKey( ItemResource, 'item' )
    position = fields.ForeignKey( PositionResource, 'position', null=True )
    contact_gel = fields.ForeignKey( ProductResource, 'contact_gel', null=True )
    solution = fields.ForeignKey( SolutionResource, 'solution', null=True )
    
    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle
    
    class Meta:
        queryset = ItemProperties.objects.all()
        resource_name = 'itemproperties'
        excludes = ['id']
        filtering = {
            'item': ALL_WITH_RELATIONS,
            'label': ALL,
            'notes': ALL,
            'position': ALL_WITH_RELATIONS,
            'contact_gel': ALL_WITH_RELATIONS,
            'solution': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

 
class RecordingPointResource( ModelResource ) :
    item = fields.ForeignKey( ItemResource, 'item' )
    class Meta:
        queryset = RecordingPoint.objects.all()
        resource_name = 'recordingpoint' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'label': ALL,
            'number': ALL,
            'item': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SubSystemResource( ModelResource ) :
    parent = fields.ForeignKey( 'self', 'parent', null=True )
    items = fields.ToManyField( ItemResource, 'items', full=True ) # after de-hydrate sub-resources are shown
    class Meta:
        queryset = SubSystem.objects.all()
        resource_name = 'subsystem'
        excludes = ['id']
        filtering = {
            'label': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SetupResource( ModelResource ) :
    place = fields.ForeignKey( OrganizationResource, 'place' )
    subsystems = fields.ToManyField( SubSystemResource, 'subsystems', null=True )
    class Meta:
        queryset = Setup.objects.all()
        resource_name = 'setup'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'room': ALL,
            'place' : ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
