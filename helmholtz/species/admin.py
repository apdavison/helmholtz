#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.species.models import Species, Strain

# overriding


class SpeciesAdmin(GuardedModelAdmin):
    pass

class StrainAdmin(GuardedModelAdmin):
    pass




# registration
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Strain, StrainAdmin)
