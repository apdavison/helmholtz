from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.units.api.resources import UnitResource

# instance
unit_resource = UnitResource()

urlpatterns = patterns('',

    url( r'^', include( unit_resource.urls ) ),

)
