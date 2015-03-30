#encoding:utf-8
from django.db import models
from django.db.models import Count
from django.core.urlresolvers import reverse

from helmholtz.people.models import Researcher
from helmholtz.devices.models import Setup
from helmholtz.preparations.models import Preparation


class Experiment( models.Model ) :
    """
    Experiment done on a :class:`Preparation` :
    ``label`` : the label identifying the experiment.
    ``type`` : the type of experiment.
    ``start`` : the start timestamp of the experiment.
    ``end`` : the end timestamp of the experiment.
    ``notes`` : notes concerning the experiment.
    ``setup`` : the setup used to make acquisition.
    ``researchers`` : researchers participating to the experiment.
    ``preparation`` : the preparation which is the subject of the experiment. 
    """
    label = models.CharField( max_length=32 )
    type = models.CharField( max_length=30, null=True, blank=True )
    start = models.DateTimeField( null=True, blank=True )
    end = models.DateTimeField( null=True, blank=True )
    notes = models.TextField( null=True, blank=True )
    setup = models.ForeignKey( Setup )
    researchers = models.ManyToManyField( Researcher )
    preparation = models.ForeignKey( Preparation, null=True, blank=True )
    
    def __unicode__(self):
        return self.label if self.label else self.pk

    def __str__(self):
        return self.__unicode__()

    @property
    def duration(self):
        """Return the duration of the :class:`Experiment` instance."""
        if self.start and self.end :
            return (self.end - self.start)
        else :
            return None
     
    def get_lab( self ) :
        labo = ''
        if self.setup.place.parent :
            labo = self.setup.place.parent.diminutive
        elif self.setup.place :
            labo = self.setup.place.diminutive
        return labo

    class Meta:
        ordering = ['-start', 'label']
        permissions = (
            ( 'view_experiment', 'Can view experiment' ),
        )

