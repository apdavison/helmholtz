from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.analysis.api.resources import DataSourceResource
from helmholtz.analysis.api.resources import StepResource
from helmholtz.analysis.api.resources import ImageResource
# instance
DataSource_resource = DataSourceResource()
Step_resource = StepResource()
Image_resource = ImageResource()

urlpatterns = patterns('',

    url( r'^', include( DataSource_resource.urls ) ),
    url( r'^', include( Step_resource.urls ) ),
    url( r'^', include( Image_resource.urls ) ),

)
