#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.storage.models import File

# overriding
class FileAdmin( GuardedModelAdmin ) :
    fields = [
        'name',
        'location',
        'mimetype',
        'original',
        'creation_date',
        'size',
        'notes'
    ]

# registration
admin.site.register( File, FileAdmin )
