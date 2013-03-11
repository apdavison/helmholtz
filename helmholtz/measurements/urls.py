from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.measurements.api.resources import ParameterResource
from helmholtz.measurements.api.resources import MeasurementResource
# instance
Parameter_resource = ParameterResource()
Measurement_resource = MeasurementResource()

urlpatterns = patterns('',

    url( r'^', include( Parameter_resource.urls ) ),
    url( r'^', include( Measurement_resource.urls ) ),

    #url( r'^(?P<resource_app>\w[\w/-]*)/(?P<resource_name>\w[\w/-]*)/(?P<pk>\w[\w/-]*)/measurement/$', 'measurements.api.resources.MeasurementResources.set_measurements' ),


)
