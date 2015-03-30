from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.stimulations.api.resources import TypeResource
from helmholtz.stimulations.api.resources import StimulusResource
from helmholtz.stimulations.api.resources import SpikeResource
from helmholtz.stimulations.api.resources import MultiResource
from helmholtz.stimulations.api.resources import DriftingGratingResource

# instance
Type_resource = TypeResource()
Stimulus_resource = StimulusResource()
Spike_resource = SpikeResource()
Multi_resource = MultiResource()
DG_resource = DriftingGratingResource()

urlpatterns = patterns('',

    url( r'^', include( Type_resource.urls ) ),
    url( r'^', include( Stimulus_resource.urls ) ),
    url( r'^', include( Spike_resource.urls ) ),
    url( r'^', include( Multi_resource.urls ) ),
    url( r'^', include( DG_resource.urls ) ),

)
