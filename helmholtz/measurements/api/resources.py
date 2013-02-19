# measurements/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField

from helmholtz.measurements.models import Parameter
from helmholtz.measurements.models import Measurement

from helmholtz.units.api.resources import UnitResource

# Allowed resources
from helmholtz.people.models import Researcher
from helmholtz.people.api.resources import ResearcherResource # example, add the others here


# Resources
class ParameterResource( ModelResource ) :
    unit = fields.ForeignKey( UnitResource, 'unit' )
    class Meta:
        queryset = Parameter.objects.all()
        resource_name = 'parameter' # optional, if not present it will be generated from classname
        filtering = {
            'label': ALL,
            'pattern': ALL,
            'type': ALL,
            'unit': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class MeasurementResource( ModelResource ) :
    parameter = fields.ForeignKey( ParameterResource, 'parameter' )
    unit = fields.ForeignKey( UnitResource, 'unit' )
    object = GenericForeignKeyField( {
        Researcher: ResearcherResource,
    }, 'object' ) # add the others here
    class Meta:
        queryset = Measurement.objects.all()
        resource_name = 'measurement'
        filtering = {
            'parameter' : ALL_WITH_RELATIONS,
            'unit' : ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
