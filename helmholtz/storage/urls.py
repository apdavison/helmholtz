from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.storage.api.resources import CommunicationProtocolResource
from helmholtz.storage.api.resources import MimeTypeResource
from helmholtz.storage.api.resources import FileServerResource
from helmholtz.storage.api.resources import FileLocationResource
from helmholtz.storage.api.resources import FileResource
# instance
CommunicationProtocol_resource = CommunicationProtocolResource()
MimeType_resource = MimeTypeResource()
FileServer_resource = FileServerResource()
FileLocation_resource = FileLocationResource()
File_resource = FileResource()

urlpatterns = patterns('',

    url( r'^', include( CommunicationProtocol_resource.urls ) ),
    url( r'^', include( MimeType_resource.urls ) ),
    url( r'^', include( FileServer_resource.urls ) ),
    url( r'^', include( FileLocation_resource.urls ) ),
    url( r'^', include( File_resource.urls ) ),

)
