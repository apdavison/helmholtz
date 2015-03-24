#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.stimulations.models import SparseNoise, TernaryDenseNoise, Type

# overriding

class SparseNoiseAdmin(GuardedModelAdmin):
    pass



class DenseNoiseAdmin(GuardedModelAdmin):
    pass

# registration
admin.site.register(SparseNoise, SparseNoiseAdmin)
admin.site.register(TernaryDenseNoise, DenseNoiseAdmin)
admin.site.register(Type)