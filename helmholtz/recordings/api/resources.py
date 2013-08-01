# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.core.api.authorization import GuardianAuthorization

from helmholtz.recordings.models import Block
from helmholtz.recordings.models import Recording
from helmholtz.recordings.models import Segment
from helmholtz.recordings.models import ContinuousSignal
from helmholtz.recordings.models import DiscreteSignal
from helmholtz.recordings.models import RecordingChannel

# Allowed resources
from helmholtz.experiments.api.resources import ExperimentResource
from helmholtz.devices.api.resources import ItemPropertiesResource
from helmholtz.stimulations.api.resources import StimulusResource
from helmholtz.storage.api.resources import FileResource


# Resources
class BlockResource( ModelResource ) :
    experiment = fields.ForeignKey( ExperimentResource, 'experiment' )
    class Meta:
        queryset = Block.objects.all()
        resource_name = 'block' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'name': ALL,
            'start': ALL,
            'end': ALL,
            'experiment': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class RecordingResource( ModelResource ) :
    block = fields.ForeignKey( BlockResource, 'block' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    stimulus = fields.ForeignKey( StimulusResource, 'stimulus', null=True )
    class Meta:
        queryset = Recording.objects.all()
        resource_name = 'recording'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'block': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
            'stimulus': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()
        authorization = GuardianAuthorization()


class SegmentResource( ModelResource ) :
    recording = fields.ForeignKey( RecordingResource, 'recording' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    class Meta:
        queryset = Segment.objects.all()
        resource_name = 'segment'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'recording': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ContinuousSignalResource( ModelResource ) :
    segment = fields.ForeignKey( SegmentResource, 'segment' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    class Meta:
        queryset = ContinuousSignal.objects.all()
        resource_name = 'continuoussignal'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'units': ALL,
            'sampling_rate': ALL,
            'start': ALL,
            'stop': ALL,
            'segment': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class DiscreteSignalResource( ModelResource ) :
    segment = fields.ForeignKey( SegmentResource, 'segment' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    class Meta:
        queryset = DiscreteSignal.objects.all()
        resource_name = 'discretesignal'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'units': ALL,
            'sampling_rate': ALL,
            'start': ALL,
            'stop': ALL,
            'segment': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class RecordingChannelResource( ModelResource ) :
    protocol = fields.ForeignKey( RecordingResource, 'protocol' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    continuous_signals = fields.ToManyField( ContinuousSignalResource, 'continuous_signals', null=True )
    configuration = fields.ForeignKey( ItemPropertiesResource, 'configuration', null=True )
    class Meta:
        queryset = RecordingChannel.objects.all()
        resource_name = 'recordingchannel'
        excludes = ['id']
        filtering = {
            'index': ALL,
            'name': ALL,
            'protocol': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
