# location/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.locations.models import Position
# other resources
from helmholtz.neuralstructures.api.resources import BrainRegionResource

# Resources
class PositionResource( ModelResource ) :
    brain_region = fields.ForeignKey( BrainRegionResource, 'brain_region' )
    class Meta:
        queryset = Position.objects.all()
        resource_name = 'position' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'label': ALL,
            'physical_meaning': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
