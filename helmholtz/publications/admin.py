from django.contrib import admin
from helmholtz.publications.models import Publication


class PublicationAdmin(admin.ModelAdmin):
    pass

# registration
admin.site.register(Publication, PublicationAdmin)
