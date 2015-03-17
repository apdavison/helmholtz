#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.preparations.models import Animal
from helmholtz.preparations.models import Preparation

# overriding
class AnimalAdmin( GuardedModelAdmin ) :
    pass
class PreparationAdmin( GuardedModelAdmin ) :
    pass


# registration
admin.site.register( Animal, AnimalAdmin )
admin.site.register( Preparation, PreparationAdmin )
