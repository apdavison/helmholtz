from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.analysis.api.resources import DataSourceResource
from helmholtz.analysis.api.resources import StepResource
# instance
DataSource_resource = DataSourceResource()
Step_resource = StepResource()

urlpatterns = patterns('',

    url( r'^', include( DataSource_resource.urls ) ),
    url( r'^', include( Step_resource.urls ) ),

)
