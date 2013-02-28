from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.stimulation.api.resources import StimulationTypeResource
from helmholtz.stimulation.api.resources import StimulusResource
from helmholtz.stimulation.api.resources import SpikeStimulusResource
from helmholtz.stimulation.api.resources import MultiStimulusResource
from helmholtz.stimulation.api.resources import DriftingGratingStimulusResource

# instance
StimulationType_resource = StimulationTypeResource()
Stimulus_resource = StimulusResource()
SpikeStimulus_resource = SpikeStimulusResource()
MultiStimulus_resource = MultiStimulusResource()
DGStimulus_resource = DriftingGratingStimulusResource()

urlpatterns = patterns('',

    url( r'^', include( StimulationType_resource.urls ) ),
    url( r'^', include( Stimulus_resource.urls ) ),
    url( r'^', include( SpikeStimulus_resource.urls ) ),
    url( r'^', include( MultiStimulus_resource.urls ) ),
    url( r'^', include( DGStimulus_resource.urls ) ),

)
