from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.devices.api.resources import ItemResource
from helmholtz.devices.api.resources import TypeResource
from helmholtz.devices.api.resources import ItemPropertiesResource
from helmholtz.devices.api.resources import RecordingPointResource
from helmholtz.devices.api.resources import SubSystemResource
from helmholtz.devices.api.resources import SetupResource
# instance
Item_resource = ItemResource()
Type_resource = TypeResource()
ItemProperties_resource = ItemPropertiesResource()
RecordingPoint_resource = RecordingPointResource()
SubSystem_resource = SubSystemResource()
Setup_resource = SetupResource()

urlpatterns = patterns('',

    url( r'^', include( Item_resource.urls ) ),
    url( r'^', include( Type_resource.urls ) ),
    url( r'^', include( ItemProperties_resource.urls ) ),
    url( r'^', include( RecordingPoint_resource.urls ) ),
    url( r'^', include( SubSystem_resource.urls ) ),
    url( r'^', include( Setup_resource.urls ) ),

)
