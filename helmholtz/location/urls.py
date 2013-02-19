from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.location.api.resources import PositionResource
# instance
Position_resource = PositionResource()

urlpatterns = patterns('',

    url( r'^', include( Position_resource.urls ) ),

)
