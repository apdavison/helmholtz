#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.units.models import Unit

# overriding
class UnitAdmin( GuardedModelAdmin ) :
    pass



# registration
admin.site.register(Unit, UnitAdmin)
