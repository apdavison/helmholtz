# analysis/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField

from helmholtz.analysis.models import DataSource
from helmholtz.analysis.models import Step
from helmholtz.analysis.models import Image
# data sources
from helmholtz.recordings.models import Block
from helmholtz.recordings.models import Recording
from helmholtz.recordings.models import ContinuousSignal
from helmholtz.recordings.models import DiscreteSignal
# and their resources
from helmholtz.recordings.api.resources import BlockResource
from helmholtz.recordings.api.resources import RecordingResource
from helmholtz.recordings.api.resources import ContinuousSignalResource
from helmholtz.recordings.api.resources import DiscreteSignalResource
# ... add here other sources

# Resources
class DataSourceResource( ModelResource ) :
    object = GenericForeignKeyField( {
        Block: BlockResource,
        Recording: RecordingResource,
        ContinuousSignal: ContinuousSignalResource,
        DiscreteSignal: DiscreteSignalResource,
    }, 'object' ) # add the others here
    class Meta:
        queryset = DataSource.objects.all()
        resource_name = 'datasource'
        excludes = ['id']
        filtering = {
            'content_type' : ALL_WITH_RELATIONS,
            'object_id' : ALL_WITH_RELATIONS,
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
        excludes = ['id']
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
        excludes = ['id']
        filtering = {
            'generator' : ALL_WITH_RELATIONS,
            'file' : ALL_WITH_RELATIONS,
            'caption' : ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
