#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.chemistry.models import Solution, Substance, Product, QuantityOfSubstance

# overriding


class SolutionAdmin(GuardedModelAdmin):
    pass

class SubstanceAdmin(GuardedModelAdmin):
    pass

class ProductAdmin(GuardedModelAdmin):
    pass

class QuantityOfSubstanceAdmin(GuardedModelAdmin):
    pass




# registration
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Substance, SubstanceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(QuantityOfSubstance, QuantityOfSubstanceAdmin)
