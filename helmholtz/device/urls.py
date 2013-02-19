from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.device.api.resources import DeviceResource
from helmholtz.device.api.resources import DeviceTypeResource
from helmholtz.device.api.resources import DevicePropertiesResource
from helmholtz.device.api.resources import RecordingPointResource
from helmholtz.device.api.resources import SubSystemResource
from helmholtz.device.api.resources import SetupResource
# instance
Device_resource = DeviceResource()
DeviceType_resource = DeviceTypeResource()
DeviceProperties_resource = DevicePropertiesResource()
RecordingPoint_resource = RecordingPointResource()
SubSystem_resource = SubSystemResource()
Setup_resource = SetupResource()

urlpatterns = patterns('',

    url( r'^', include( Device_resource.urls ) ),
    url( r'^', include( DeviceType_resource.urls ) ),
    url( r'^', include( DeviceProperties_resource.urls ) ),
    url( r'^', include( RecordingPoint_resource.urls ) ),
    url( r'^', include( SubSystem_resource.urls ) ),
    url( r'^', include( Setup_resource.urls ) ),

)
