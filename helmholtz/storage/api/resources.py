# species/api.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.core.authorization import GuardianAuthorization

from helmholtz.storage.models import CommunicationProtocol
from helmholtz.storage.models import MimeType
from helmholtz.storage.models import FileServer
from helmholtz.storage.models import FileLocation
from helmholtz.storage.models import File


# Resources
class CommunicationProtocolResource( ModelResource ) :
    class Meta:
        queryset = CommunicationProtocol.objects.all()
        resource_name = 'communicationprotocol' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'name': ALL,
            'initials': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class MimeTypeResource( ModelResource ) :
    class Meta:
        queryset = MimeType.objects.all()
        resource_name = 'mimetype'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'extension': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class FileServerResource( ModelResource ) :
    protocol = fields.ForeignKey( CommunicationProtocolResource, 'protocol' )
    class Meta:
        queryset = FileServer.objects.all()
        resource_name = 'fileserver'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'protocol': ALL_WITH_RELATIONS,
            'ip_address': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class FileLocationResource( ModelResource ) :
    server = fields.ForeignKey( FileServerResource, 'server' )
    class Meta:
        queryset = FileLocation.objects.all()
        resource_name = 'filelocation'
        excludes = ['id']
        filtering = {
            'server': ALL_WITH_RELATIONS,
            'drive': ALL,
            'path': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class FileResource( ModelResource ) :
    location = fields.ForeignKey( FileLocationResource, 'location' )
    mimetype = fields.ForeignKey( MimeTypeResource, 'mimetype' )
    class Meta:
        queryset = File.objects.all()
        resource_name = 'file'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'location': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()
        authorization = GuardianAuthorization()
