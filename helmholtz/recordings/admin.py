#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.recordings.models import Block, Recording

# overriding

class BlockAdmin(GuardedModelAdmin):
    pass

class RecordingAdmin( GuardedModelAdmin ) :
    fields = [
        'block',
        'name',
        'file',
        'rec_datetime',
        'description',
        'is_continuous',
        'stimulus'
    ]

# registration
admin.site.register(Block, BlockAdmin)
admin.site.register(Recording, RecordingAdmin)
