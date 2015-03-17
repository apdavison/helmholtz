#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.neuralstructures.models import BrainRegion, CellType, Cell


class CellTypeAdmin(admin.ModelAdmin):
    pass

class BrainRegionAdmin(admin.ModelAdmin):
    pass

class CellAdmin(GuardedModelAdmin):
    pass


# registration
admin.site.register(BrainRegion, BrainRegionAdmin)
admin.site.register(CellType, CellTypeAdmin)
admin.site.register(Cell, CellAdmin)
