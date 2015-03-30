#encoding:utf-8
from django.db import models
from helmholtz.core.models import HierarchicalStructure 
from helmholtz.species.models import Species

class BrainRegion( HierarchicalStructure ) :
    """A subset of Neurolex brain regions."""
    id = models.CharField( primary_key=True, max_length=20, help_text="neurolex unique identifier" )
    name = models.CharField( max_length=100 )
    abbreviation = models.CharField( max_length=10, null=True, blank=True )
    parent = models.ForeignKey( 'self', null=True, blank=True )
    species = models.ManyToManyField( Species )
    url = models.URLField( null=True, blank=True, help_text="neurolex description web page" )
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    @property
    def name_or_abbreviation(self):
        return self.abbreviation if self.abbreviation else self.name


class CellType( models.Model ):
    """A subset of Neurolex cell types."""
    id = models.CharField( primary_key=True, max_length=20, help_text="neurolex unique identifier" )
    name = models.CharField( max_length=100 )
    brain_regions = models.ManyToManyField( BrainRegion, null=True, blank=True )
    url = models.URLField( null=True, blank=True, help_text="neurolex description web page" )
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Cell( models.Model ):
    """Cell from which raw data are acquired."""
    label = models.CharField( max_length=8, null=True, blank=True )
    type = models.ForeignKey( CellType, null=True )
    properties = models.TextField( null=True, blank=True )
    
    def mapping(self, field_name):
        mapping = {'block':'B'}
        return mapping(field_name)
