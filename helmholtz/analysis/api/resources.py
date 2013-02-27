# measurements/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField

from helmholtz.analysis.models import DataSource
from helmholtz.analysis.models import Step
from helmholtz.analysis.models import Image
from helmholtz.recording.models import ContinuousSignal
from helmholtz.recording.models import DiscreteSignal
# allowed resources
from helmholtz.recording.api.resources import ContinuousSignalResource
from helmholtz.recording.api.resources import DiscreteSignalResource
# ... add here other sources

# Resources
class DataSourceResource( ModelResource ) :
    object = GenericForeignKeyField( {
        ContinuousSignal: ContinuousSignalResource,
        DiscreteSignal: DiscreteSignalResource,
    }, 'object' ) # add the others here
    class Meta:
        queryset = DataSource.objects.all()
        resource_name = 'datasource'
        filtering = {
            'object' : ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]


class StepResource( ModelResource ) :
    inputs = fields.ToManyField( DataSourceResource, 'inputs', null=True )
    outputs = fields.ToManyField( DataSourceResource, 'outputs', null=True )
    class Meta:
        queryset = Step.objects.all()
        resource_name = 'step'
        filtering = {
            'inputs' : ALL_WITH_RELATIONS,
            'outputs' : ALL_WITH_RELATIONS,
            'algorithm' : ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]


class ImageResource( ModelResource ) :
    generator = fields.ForeignKey( StepResource, 'generator', null=True )
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'image'
        filtering = {
            'generator' : ALL_WITH_RELATIONS,
            'file' : ALL_WITH_RELATIONS,
            'caption' : ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
