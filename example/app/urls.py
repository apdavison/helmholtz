from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # attach measurements
    url( r'^(?P<resource_name>\w[\w/-]*)/(?P<pk>\w[\w/-]*)/measurement/$', 'helmholtz.measurements.api.resources.set_measurement_by_name' ),
    url( r'^(?P<resource_app>\w[\w/-]*)/(?P<resource_name>\w[\w/-]*)/(?P<pk>\w[\w/-]*)/measurement/$', 'helmholtz.measurements.api.resources.set_measurement' ),
    # APPS
    ('^people/', include('helmholtz.people.urls')),
    ('^species/', include('helmholtz.species.urls')),
    ('^units/', include('helmholtz.units.urls')),
    ('^storage/', include('helmholtz.storage.urls')),
    ('^measurements/', include('helmholtz.measurements.urls')),
    ('^', include('helmholtz.neuralstructures.urls')), # to have cell as a base address
    ('^neuralstructures/', include('helmholtz.neuralstructures.urls')), # to have all others (as well as cell)
    ('^chemistry/', include('helmholtz.chemistry.urls')),
    ('^locations/', include('helmholtz.locations.urls')),
    ('^devices/', include('helmholtz.devices.urls')),
    ('^stimulations/', include('helmholtz.stimulations.urls')),
    ('^preparations/', include('helmholtz.preparations.urls')),
    ('^', include('helmholtz.experiments.urls')), # to have experiments as a base address
    ('^drugs/', include('helmholtz.drugs.urls')),
    ('^recordings/', include('helmholtz.recordings.urls')),
    ('^analysis/', include('helmholtz.analysis.urls')),

)
