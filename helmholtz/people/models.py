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


class ScientificStructure( HierarchicalStructure ) :
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
    
    @property
    def manager(self):
        """Return the manager a of the :class:`ScientificStructure` instance."""
        positions = self.position_set.filter(position_type__name="manager")
        return positions.latest('start').researcher if positions else None
    
    def _years(self):
        """Age of the :class:`ScientificStructure` instance in years."""
        today = date.today()
        _end = self.dissolution_date or today
        if self.foundation_date :
            return int(round((_end - self.foundation_date).days / 365.25))
        else:
            return None
    years = property(_years)
    
    def get_main_and_sub_structures(self):
        _main = self.get_root()
        _sub = self if (_main != self) else None
        return _main, _sub
    
    def create_diminutive(self, separator="_"):
        """
        Return an auto generated diminutive from the
        name of the :class:`ScientificStructure` instance.
        """
        if not self.diminutive:
            self.diminutive = self.name.replace(" ", separator)
    
    @property
    def researchers(self):
        """
        Return :class:`django.contrib.auth.models.Researchers`
        instances corresponding to the :class:`ScientificStructure`
        instance and its children.
        """
        structures = list()
        structures.append(self)
        structures.extend(self.get_children(True, False))
        researchers = Researcher.objects.filter(position__structure__in=structures).order_by('last_name','first_name').distinct()
        return researchers
    
    @property
    def structures(self):
        return self.get_children(True, True)
    
    @property
    def experiments(self):
        """
        Return :class:`Experiment` instances provided
        by the :class:`ScientificStructure` instance.
        """
        q1 = models.Q(setup__place__parent=self)
        q2 = models.Q(setup__place=self)
        cls = get_class('experiment', 'Experiment')
        return cls.objects.filter(q1 | q2).distinct()
    
    def number_of_researchers(self):
        """
        Get the number of :class:`Researcher` instances
        working in the :class:`ScientificStructure` instance.
        """
        aggregate = self.position_set.all().aggregate(Count("researcher", distinct=True))
        count = aggregate["researcher__count"]
        if self.scientificstructure_set.count :
            for children in self.get_children(recursive=False) :
                count += children.number_of_researchers()
        return count
    
    def get_groups(self, recursive=False):
        """
        Return :class:`django.contrib.auth.models.Group`
        instances corresponding to the :class:`ScientificStructure`
        instance and its children.
        """
        groups = list()
        groups.append(self.db_group.name)
        if recursive :
            groups = [k.db_group.name for k in self.get_children(recursive)]
        return Group.objects.filter(name__in=groups)
    
    

class Researcher( models.Model ):
    """
    Anybody working in a :class:`ScientificStructure`.
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
        st = "%s %s" % ( self.user.first_name, self.user.last_name )
        st += "%s %s %s" % ( self.postal_code, self.town, self.state )
        if self.state :
            st += " (%s)" % self.country
        return st  
    
    def get_full_name(self):
        """
        Get the full name of the :class:`Researcher` instance, 
        i.e. the combination between its first and last names.
        """
        return "%s %s" % (self.first_name, self.last_name)
    
    def position_in_structure(self, structure):
        """
        Return the latest :class:`Position` of the 
        :class:`Researcher` instance for the specified
        :class:`ScientificStructure`.
        """
        structures = list()
        structures.append(structure)
        structures.extend(structure.get_children(True, False))
        positions = self.position_set.filter(structure__in=structures)
        position = positions.latest('start') if positions else None
        return position
    
    def current_position(self):
        """
        Return the current :class:`Position` of the 
        :class:`Researcher` instance.
        """
        today = date.today()
        last_position = self.last_position()
        if last_position :
            if not last_position.end or ((last_position.start <= today) and (last_position.end >= today)) :
                return last_position
        return None
    
    def last_position(self, structure=None):
        """
        Return the last effective :class:`Position` of
        the :class:`Researcher` instance in the specified
        :class:`ScientificStructure`.
        """
        if structure :
            structures = list()
            structures.append(structure)
            structures.extend(structure.get_children(True, False))
            positions = self.position_set.filter(structure__in=structures)
        else :
            positions = self.position_set.all()
        return positions.latest("start") if positions else None
    
    def number_of_structures(self):
        """
        Get the number of :class:`ScientificStructure`
        where a :class:`Researcher` has worked.
        """
        aggregate = self.position_set.all().aggregate(Count("structure", distinct=True))
        return aggregate["structure__count"]
    
 

class Position( models.Model ) :
    """
    Contract linking a :class:`Researcher` to a :class:`ScientificStructure`.
    
    NB : this class brings more flexibility by separating people 
    descriptions from their positions in a hierarchical structure.
    """
    researcher = models.ForeignKey( Researcher )
    structure = models.ForeignKey( ScientificStructure )
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
    
    
    class Meta:
        ordering = ['name']
