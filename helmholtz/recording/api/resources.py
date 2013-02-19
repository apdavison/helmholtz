# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.recording.models import RecordingBlock
from helmholtz.recording.models import ProtocolRecording
from helmholtz.recording.models import Segment
from helmholtz.recording.models import ContinuousSignal
from helmholtz.recording.models import DiscreteSignal
from helmholtz.recording.models import RecordingChannel

# Allowed resources
from helmholtz.experiment.api.resources import ExperimentResource
from helmholtz.device.api.resources import DevicePropertiesResource
from helmholtz.stimulation.api.resources import SpikeStimulusResource
from helmholtz.storage.api.resources import FileResource


# Resources
class RecordingBlockResource( ModelResource ) :
    experiment = fields.ForeignKey( ExperimentResource, 'experiment' )
    class Meta:
        queryset = RecordingBlock.objects.all()
        resource_name = 'recordingblock' # optional, if not present it will be generated from classname
        filtering = {
            'name': ALL,
            'start': ALL,
            'end': ALL,
            'experiment': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ProtocolRecordingResource( ModelResource ) :
    block = fields.ForeignKey( RecordingBlockResource, 'block' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    stimulus = fields.ForeignKey( SpikeStimulusResource, 'stimulus', null=True )
    class Meta:
        queryset = ProtocolRecording.objects.all()
        resource_name = 'protocolrecording'
        filtering = {
            'name': ALL,
            'block': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
            'stimulus': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SegmentResource( ModelResource ) :
    recording = fields.ForeignKey( ProtocolRecordingResource, 'recording' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    class Meta:
        queryset = Segment.objects.all()
        resource_name = 'segment'
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
    protocol = fields.ForeignKey( ProtocolRecordingResource, 'protocol' )
    file = fields.ForeignKey( FileResource, 'file', null=True )
    continuous_signals = fields.ToManyField( ContinuousSignalResource, 'continuous_signals', null=True )
    configuration = fields.ForeignKey( DevicePropertiesResource, 'configuration', null=True )
    class Meta:
        queryset = RecordingChannel.objects.all()
        resource_name = 'recordingchannel'
        filtering = {
            'index': ALL,
            'name': ALL,
            'protocol': ALL_WITH_RELATIONS,
            'file': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
