#encoding:utf-8
import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from helmholtz.species.models import Strain
from helmholtz.people.models import Supplier
from helmholtz.devices.models import Item
from helmholtz.measurements.models import Measurement
from helmholtz.chemistry.models import Solution

"""
This module provides a set of classes useful to track
animals living in a laboratory and used for experimentation.
"""

class Animal( models.Model ) :
    """Animal that is the subject of an :class:`Experiment`."""
    strain = models.ForeignKey( Strain, null=True )
    identifier = models.CharField( max_length=15, null=True, blank=True )
    nickname = models.CharField( max_length=15, null=True, blank=True )
    sex = models.CharField( max_length=1, choices=(('M', 'male'), ('F', 'female')), null=True, blank=True )
    birth = models.DateField( help_text="(approximate)", null=True, blank=True )
    sacrifice = models.DateField( null=True, blank=True )
    supplier = models.ForeignKey( Supplier, null=True, blank=True ) 
    
    def __unicode__(self):
        st = ''
        if self.identifier :
            st += self.identifier
        if self.strain :
            if self.identifier :
                st += ', '
            st += "%s" % (self.strain)
        return st 

    def __str__(self):
        return self.__unicode__()

    class Meta:
        permissions = (
            ( 'view_animal', 'Can view animal' ),
        )
        ordering = ['-sacrifice']


preparations = (
    ( 'IN-VIVO-SHARP', 'in vivo sharp' ),
    ( 'IN-VIVO-PATCH', 'in vivo patch' ),
    ( 'IN-VITRO-CULTURE', 'in vitro culture' ),
    ( 'IN-VITRO-SLICE', 'in vitro slice' ),
    ( 'IN-SILICO', 'in silico' )
)
class Preparation( models.Model ):
    """The subject of an :class:`Experiment`."""
    animal = models.ForeignKey( Animal, null=True, blank=True )
    type = models.CharField( max_length=16, choices=preparations, null=True, blank=True, verbose_name="types of preparation" )
    protocol = models.TextField( null=True, blank=True )   
    equipment = models.ForeignKey( Item, null=True, blank=True )
    model_description = models.TextField( null=True, blank=True ) # simulation
    thickness = models.FloatField( null=True ) # microm &mu;m
    cut_orientation = models.CharField( max_length=50, null=True, blank=True )
    cutting_solution = models.ForeignKey( Solution, related_name="is_cutting_solution_of", null=True, blank=True )
    bath_solution = models.ForeignKey( Solution, related_name="is_bath_solution_of", null=True, blank=True )
    notes = generic.GenericRelation( Measurement, verbose_name="observations", content_type_field='content_type', object_id_field='object_id' )
    
    def __unicode__(self):
        return u"%s, %s" % (self.type, self.animal)

    def __str__(self):
        return self.__unicode__()