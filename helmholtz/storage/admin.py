#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.storage.models import File, FileLocation, FileServer, MimeType, CommunicationProtocol

# overriding
class FileAdmin(GuardedModelAdmin):
    fields = [
        'name',
        'location',
        'mimetype',
        'original',
        'creation_date',
        'size',
        'notes'
    ]

class FileLocationAdmin(GuardedModelAdmin):
    pass

class FileServerAdmin(GuardedModelAdmin):
    pass

class MimeTypeAdmin(GuardedModelAdmin):
    pass

class CommunicationProtocolAdmin(GuardedModelAdmin):
    pass



# registration
admin.site.register(File, FileAdmin)
admin.site.register(FileLocation, FileLocationAdmin)
admin.site.register(FileServer, FileServerAdmin)
admin.site.register(MimeType, MimeTypeAdmin)
admin.site.register(CommunicationProtocol, CommunicationProtocolAdmin)
