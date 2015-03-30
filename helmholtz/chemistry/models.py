#encoding:utf-8
from django.db import models
from helmholtz.people.models import Supplier

"""
This module provides models useful to track substances used during experiments.
"""

class Substance( models.Model ):
    """
    Substance used during an :class:`Experiment` :
    
    ``name`` : the identifier of the substance.
    
    """
    name = models.CharField( primary_key=True, max_length=32 )
    
    def __unicode__(self):
        return u"%s" % (self.name)
    shortname = property(__unicode__)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['name']


class Product( models.Model ):
    """
    Product delivered by a :class:`Supplier` :
    
    ``catalog_ref`` : the catalog reference of a product.
    ``name`` : the name of the product.
    ``substance`` : the substance provided by the product.
    ``supplier`` : the supplier providing the product.
    
    """
    catalog_ref = models.CharField( max_length=50, null=True, blank=True )# maybe CAS reference should be more useful than the supplier ? 
    name = models.CharField( max_length=256 )
    substance = models.ForeignKey( Substance, null=True, blank=True )
    supplier = models.ForeignKey( Supplier, null=True, blank=True )
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta : 
        unique_together = (("name", "supplier"),)


class Solution( models.Model ):
    """
    Solution used in :class:`DrugApplication`, :class:`HollowElectrodeConfiguration'
    and :class:`ÌnVitroSlice` models :
    
    ``label`` : the identifier of the solution.
    
    """
    label = models.CharField( primary_key=True, max_length=256 )

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.__unicode__()

    def enumerate_components(self):
        """Return a string enumerating components of the :class:`Solution` instance."""
        components = [k.__unicode__() for k in self.quantityofsubstance.all()]
        return ','.join(components) if components else None
    
    def list_components(self):
        """
        Return a list of names of the chemical components of this
        solution and their concentrations.
        """
        return ["%s %s" % (s.concentration, s.chemical_product.name) for s in self.quantityofsubstance_set.all()]


class QuantityOfSubstance( models.Model ):
    """
    Store the actual composition of a :class:`Solution` :
    
    ``solution`` : the solution that is decomposed by several chemical products.
    ``chemical_product`` : a chemical product composing a solution.
    ``concentration`` : the concentration of a chemical product composing the solution
    
    """
    solution = models.ForeignKey( Solution )
    chemical_product = models.ForeignKey( Product )
    concentration = models.FloatField()

    class Meta :
        unique_together = (('solution', 'chemical_product'),)
    
    def __unicode__(self):
        return "%s %s mol/L" % (self.chemical_product, self.concentration)

    def __str__(self):
        return self.__unicode__()
