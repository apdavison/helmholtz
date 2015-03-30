from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.recordings.api.resources import BlockResource
from helmholtz.recordings.api.resources import RecordingResource
from helmholtz.recordings.api.resources import SegmentResource
from helmholtz.recordings.api.resources import ContinuousSignalResource
from helmholtz.recordings.api.resources import DiscreteSignalResource
from helmholtz.recordings.api.resources import RecordingChannelResource

# instance
Block_resource = BlockResource()
Recording_resource = RecordingResource()
Segment_resource = SegmentResource()
ContinuousSignal_resource = ContinuousSignalResource()
DiscreteSignal_resource = DiscreteSignalResource()
RecordingChannel_resource = RecordingChannelResource()

urlpatterns = patterns('',

    url( r'^', include( Block_resource.urls ) ),
    url( r'^', include( Recording_resource.urls ) ),
    url( r'^', include( Segment_resource.urls ) ),
    url( r'^', include( ContinuousSignal_resource.urls ) ),
    url( r'^', include( DiscreteSignal_resource.urls ) ),
    url( r'^', include( RecordingChannel_resource.urls ) ),

)
