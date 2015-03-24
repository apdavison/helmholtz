#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.drugs.models import ContinuousDrugApplication, DiscreteDrugApplication

# overriding
# class FileAdmin(GuardedModelAdmin):
#     fields = [
#         'name',
#         'location',
#         'mimetype',
#         'original',
#         'creation_date',
#         'size',
#         'notes'
#     ]



class ContinuousDrugApplicationAdmin(GuardedModelAdmin):
    pass

class DiscreteDrugApplicationAdmin(GuardedModelAdmin):
    pass



# registration
admin.site.register(ContinuousDrugApplication, ContinuousDrugApplicationAdmin)
admin.site.register(DiscreteDrugApplication, DiscreteDrugApplicationAdmin)
