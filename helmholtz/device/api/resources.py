# device/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.device.models import Device
from helmholtz.device.models import DeviceType
from helmholtz.device.models import DeviceProperties
from helmholtz.device.models import RecordingPoint
from helmholtz.device.models import SubSystem
from helmholtz.device.models import Setup

# Allowed resources
from helmholtz.people.api.resources import ScientificStructureResource # example, add the others here
from helmholtz.people.api.resources import SupplierResource
from helmholtz.location.api.resources import PositionResource
from helmholtz.chemistry.api.resources import SolutionResource
from helmholtz.chemistry.api.resources import ProductResource


# Resources
class DeviceTypeResource( ModelResource ) :
    class Meta:
        queryset = DeviceType.objects.all()
        resource_name = 'devicetype' # optional, if not present it will be generated from classname
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class DeviceResource( ModelResource ) :
    type = fields.ForeignKey( DeviceTypeResource, 'type' )
    manufacturer = fields.ForeignKey( SupplierResource, 'manufacturer', null=True )
    
    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle
    
    class Meta:
        queryset = Device.objects.all()
        resource_name = 'device'
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

 
class DevicePropertiesResource( ModelResource ) :
    device = fields.ForeignKey( DeviceResource, 'device' )
    position = fields.ForeignKey( PositionResource, 'position', null=True )
    contact_gel = fields.ForeignKey( ProductResource, 'contact_gel', null=True )
    solution = fields.ForeignKey( SolutionResource, 'solution', null=True )
    
    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle
    
    class Meta:
        queryset = DeviceProperties.objects.all()
        resource_name = 'deviceproperties'
        filtering = {
            'device': ALL_WITH_RELATIONS,
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
    device = fields.ForeignKey( DeviceResource, 'device' )
    class Meta:
        queryset = RecordingPoint.objects.all()
        resource_name = 'recordingpoint' # optional, if not present it will be generated from classname
        filtering = {
            'label': ALL,
            'number': ALL,
            'device': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SubSystemResource( ModelResource ) :
    parent = fields.ForeignKey( 'self', 'parent', null=True )
    devices = fields.ToManyField( DeviceResource, 'devices', full=True ) # after de-hydrate sub-resources are shown
    class Meta:
        queryset = SubSystem.objects.all()
        resource_name = 'subsystem'
        filtering = {
            'label': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SetupResource( ModelResource ) :
    place = fields.ForeignKey( ScientificStructureResource, 'place' )
    subsystems = fields.ToManyField( SubSystemResource, 'subsystems' )
    class Meta:
        queryset = Setup.objects.all()
        resource_name = 'setup'
        filtering = {
            'label': ALL,
            'room': ALL,
            'place' : ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
