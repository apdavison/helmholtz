# analysis/api/resources.py
import re
from django.contrib.contenttypes.models import ContentType

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField

from helmholtz.core.authorization import GuardianAuthorization

from helmholtz.analysis.models import DataSource
from helmholtz.analysis.models import Step
from helmholtz.analysis.models import Image
# data sources
from helmholtz.recordings.models import Block
from helmholtz.recordings.models import Recording
from helmholtz.recordings.models import Segment
from helmholtz.recordings.models import ContinuousSignal
from helmholtz.recordings.models import DiscreteSignal
# and their resources
from helmholtz.recordings.api.resources import BlockResource
from helmholtz.recordings.api.resources import RecordingResource
from helmholtz.recordings.api.resources import SegmentResource
from helmholtz.recordings.api.resources import ContinuousSignalResource
from helmholtz.recordings.api.resources import DiscreteSignalResource
# ... add here other sources

# Resources
class DataSourceResource( ModelResource ) :
    object = GenericForeignKeyField( {
        Block: BlockResource,
        Recording: RecordingResource,
        Segment: SegmentResource,
        ContinuousSignal: ContinuousSignalResource,
        DiscreteSignal: DiscreteSignalResource,
    }, 'object' ) # add the others here
    class Meta:
        queryset = DataSource.objects.all()
        resource_name = 'datasource'
        excludes = ['id']
        filtering = {
            'object' : ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


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
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


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
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()
        authorization = GuardianAuthorization()
