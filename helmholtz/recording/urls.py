from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.recording.api.resources import RecordingBlockResource
from helmholtz.recording.api.resources import ProtocolRecordingResource
from helmholtz.recording.api.resources import SegmentResource
from helmholtz.recording.api.resources import ContinuousSignalResource
from helmholtz.recording.api.resources import DiscreteSignalResource
from helmholtz.recording.api.resources import RecordingChannelResource

# instance
RecordingBlock_resource = RecordingBlockResource()
ProtocolRecording_resource = ProtocolRecordingResource()
Segment_resource = SegmentResource()
ContinuousSignal_resource = ContinuousSignalResource()
DiscreteSignal_resource = DiscreteSignalResource()
RecordingChannel_resource = RecordingChannelResource()

urlpatterns = patterns('',

    url( r'^', include( RecordingBlock_resource.urls ) ),
    url( r'^', include( ProtocolRecording_resource.urls ) ),
    url( r'^', include( Segment_resource.urls ) ),
    url( r'^', include( ContinuousSignal_resource.urls ) ),
    url( r'^', include( DiscreteSignal_resource.urls ) ),
    url( r'^', include( RecordingChannel_resource.urls ) ),

)
