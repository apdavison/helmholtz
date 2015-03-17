#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.analysis.models import Image, DataSource, Step

# overriding
class ImageAdmin( GuardedModelAdmin ) :
    fields = [ 'generator', 'file', 'caption' ]

class DataSourceAdmin(GuardedModelAdmin):
    pass
    #fields = [ 'generator', 'file', 'caption' ]


class StepAdmin(GuardedModelAdmin):
    pass
    #fields = [ 'generator', 'file', 'caption' ]

# registration
admin.site.register( Image, ImageAdmin )
admin.site.register( DataSource, DataSourceAdmin )
admin.site.register( Step, StepAdmin )