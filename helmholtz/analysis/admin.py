#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.analysis.models import Image

# overriding
class ImageAdmin( GuardedModelAdmin ) :
    fields = [ 'generator', 'file', 'caption' ]

# registration
admin.site.register( Image, ImageAdmin )
