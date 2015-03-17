from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.experiments.api.resources import ExperimentResource
# instance
Experiment_resource = ExperimentResource()

urlpatterns = patterns('',

    url( r'^', include( Experiment_resource.urls ) ),

)
