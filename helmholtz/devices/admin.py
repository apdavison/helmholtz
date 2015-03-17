#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.devices.models import Type, Item, ItemProperties, RecordingPoint, SubSystem, Setup

# overriding


class TypeAdmin(GuardedModelAdmin):
    pass

class ItemAdmin(GuardedModelAdmin):
    pass

class ItemPropertiesAdmin(GuardedModelAdmin):
    pass

class RecordingPointAdmin(GuardedModelAdmin):
    pass

class SubSystemAdmin(GuardedModelAdmin):
    pass

class SetupAdmin(GuardedModelAdmin):
    pass


# registration
admin.site.register(Type, TypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemProperties, ItemPropertiesAdmin)
admin.site.register(RecordingPoint, RecordingPointAdmin)
admin.site.register(SubSystem, SubSystemAdmin)
admin.site.register(Setup, SetupAdmin)
