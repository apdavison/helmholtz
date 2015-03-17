#encoding:utf-8

#Here's some usecases :
# 1 - define a laboratory, its hierarchical organization, specificities and research axes
# 2 - store information useful to contact people or their relative laboratory to ask more explanations concerning experiments 
# 3 - set the list of people that have been hired by a laboratory and that have collaborated on experiments
# 4 - track in time someone's position
# 5 - define more accurately the profile of a user
from datetime import date
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes import generic

from helmholtz.core.models import Cast
from helmholtz.core.models import HierarchicalStructure
from helmholtz.core.shortcuts import get_class
from helmholtz.core.shortcuts import get_subclasses

from helmholtz.measurements.models import Measurement


class Organization( HierarchicalStructure ) :
    """Hierarchical structure representing a large variety of scientific structures.
    
    NB : The db_group parameter specifies the group relative to a scientific structure. 
    Consequently, it is possible to implement a hierarchical user administration.
    """
    diminutive = models.CharField( max_length=32 ) # Not all structures have acronyms
    name = models.CharField( max_length=256 )
    parent = models.ForeignKey( 'self', null=True, blank=True )
    is_data_provider = models.BooleanField( default=False, null=False, blank=False )
    foundation_date = models.DateField( null=True, blank=True )
    dissolution_date = models.DateField( null=True, blank=True )
    description = models.TextField( null=True, blank=True )
    db_group = models.OneToOneField( Group, verbose_name="database group", null=True, blank=True )
    
    class Meta :
        ordering = ['name']
    
    def __unicode__( self, separator=u" \u2192 " ) :
        complete_path = self.diminutive or self.name
        if self.parent:
            complete_path = u"%s%s%s" % (self.parent.__unicode__(separator=separator), separator, complete_path)
        return complete_path

    def __str__(self):
        return self.__unicode__()
    

class Researcher( models.Model ):
    """
    Anybody working in a :class:`Organization`.
    Used as a profile for a database :class:`django.contrib.auth.models.User`.
    """
    user = models.OneToOneField( User, null=True, blank=True, verbose_name="database user" )
    phone = models.CharField( max_length=16 )
    website = models.URLField( max_length=256 )
    street_address = models.CharField( max_length=256 )
    postal_code = models.CharField( max_length=10 )
    town = models.CharField( max_length=256 )
    state = models.CharField( max_length=256, null=True, blank=True )
    country = models.CharField( max_length=256 )
    notes = models.TextField( null=True, blank=True )
    
    def __unicode__(self):
        if self.user.last_name:
            st = "%s %s" % ( self.user.first_name, self.user.last_name )
        else:
            st = self.user.username
        return st  

    def __str__(self):
        return self.__unicode__()

    class Meta:
        permissions = (
            ( 'view_researcher', 'Can view researcher' ),
        )

 

class Position( models.Model ) :
    """
    Contract linking a :class:`Researcher` to a :class:`Organization`.
    
    NB : this class brings more flexibility by separating people 
    descriptions from their positions in a hierarchical structure.
    """
    researcher = models.ForeignKey( Researcher )
    structure = models.ForeignKey( Organization )
    type = models.CharField( max_length=256 )
    start = models.DateField()
    end = models.DateField( null=True )
    notes = models.TextField( null=True, blank=True )
     
    class Meta:
        ordering = ['-start', 'structure', 'researcher']
        
    def __unicode__(self):
        end = self.end or "present"
        st = u"%s, %s in %s from %s to %s" % (self.researcher, self.type, self.structure, self.start, end)
        return st

    def __str__(self):
        return self.__unicode__()


class Supplier(models.Model):
    """Supplier of resources used in a laboratory."""
    name = models.CharField(max_length=250, primary_key=True)
    phone = models.CharField( max_length=16 )
    website = models.URLField( max_length=256 )
    street_address = models.CharField(max_length=256, verbose_name="address 1")
    postal_code = models.CharField(max_length=10)
    town = models.CharField(max_length=256)
    state = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256)
    notes = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        st = "%s" % ( self.name )
        st += "%s %s %s" % ( self.postal_code, self.town, self.state )
        if self.state :
            st += " (%s)" % self.country
        return st  

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['name']
