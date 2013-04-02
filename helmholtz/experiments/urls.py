from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.experiments.api.resources import ExperimentResource
# instance
Experiment_resource = ExperimentResource()

urlpatterns = patterns('',

    url( r'^', include( Experiment_resource.urls ) ),

)
