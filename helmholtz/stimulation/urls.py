from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.stimulation.api.resources import StimulationTypeResource
from helmholtz.stimulation.api.resources import SpikeStimulusResource

# instance
StimulationType_resource = StimulationTypeResource()
SpikeStimulus_resource = SpikeStimulusResource()

urlpatterns = patterns('',

    url( r'^', include( StimulationType_resource.urls ) ),
    url( r'^', include( SpikeStimulus_resource.urls ) ),

)
