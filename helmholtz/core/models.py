#encoding:utf-8

# models.py
# Contains classes to handle data:
# - cast query results into specific classes and subclasses
# - access hierarchically trees of classes

from django.db import models
#from django.db.models import signals #TODO: reimport when worked out
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.datastructures import SortedDict
from helmholtz.core.schema import get_pk_type
from helmholtz.core.schema import foreign_keys
from helmholtz.core.schema import many_to_many_fields
from helmholtz.core.schema import reverse_foreign_keys
from helmholtz.core.schema import reverse_many_to_many_fields
from helmholtz.core.schema import get_base_class

class CastQuerySet(models.query.QuerySet):
    """
    A subclass of :class:`QuerySet` useful to retrieve from
    a queryset the objects corresponding to the same subclass.
    """
    
    def cast(self, entity):
        """Return a :class:`QuerySet` containing all objects of the same specified subclass."""
        subclasses = self.model.get_subclasses_recursively(False)

        if isinstance(entity, str) :
            names = [k.__name__ for k in subclasses]
            index = names.index(entity)
        else :
            index = subclasses.index(entity)
        if (subclasses[index] != self.model) :
            selection = subclasses[index]
            lookup = selection.subclass_lookup(base_class=self.model)
            dct = {'%s__isnull' % lookup:False}
            pks = [k.id for k in self.filter(**dct).distinct()]
            objects = selection.objects.filter(pk__in=pks)
        else :
            objects = self
        
        return objects
    
class CastManager(models.Manager):
    """A subclass of :class:`Manager` useful to cast objects to their actual type."""
    
    def get_queryset(self):
        """Return a :class:`CastQuerySet`."""
        return CastQuerySet(self.model, using=self._db)
    
    def cast(self, entity):
        """Return a :class:`QuerySet` containing all objects of the same specified subclass."""
        return self.get_queryset().cast(entity)

class Cast(models.Model):
    """An abstract class telling that an object could be casted to the leaf node of a class hierarchy."""
    
    objects = CastManager()
    
    def sub_classes(self):
        """Return a list containing all lower cased subclass names."""
        return [k.__name__.lower() for k in self.__subclasses__()]
    
    @classmethod
    def get_subclasses(cls, proxies=False):
        """Get subclasses of a class."""
        if proxies :
            return cls.__subclasses__()
        else :
            return [k for k in cls.__subclasses__() if (k._meta.proxy == False)]
    
    @classmethod
    def get_subclasses_recursively(cls, strict=True, proxies=False):
        """Get recursively subclasses of a class."""
        subclasses = list()
        for subclass in cls.get_subclasses(proxies) :
            subclasses.append(subclass)
            subclasses.extend(subclass.get_subclasses_recursively(proxies=proxies))
        if not strict :
            subclasses.insert(0, cls)    
        return subclasses
    
    @classmethod
    def get_parents_recursively(cls):
        """Get the superclasses chain of a class."""
        result = list()
        for parent in cls._meta.parents :
            result.append(parent)
            result.extend(parent.get_parents_recursively())
        return result
    
    @classmethod
    def get_base_class(cls):
        """Get the base superclass of a class."""
        parents = cls.get_parents_recursively() 
        return parents[-1] if parents else cls
    
    @classmethod
    def subclass_lookup(cls, base_class=None):
        """Get the entire lookup from the base class to the target subclass."""
        parents = cls.get_parents_recursively()
        index = -1 if not base_class else parents.index(base_class)
        chain = parents[0:index]
        chain.reverse()
        chain.append(cls)
        lookup = '__'.join([k.__name__.lower() for k in chain])
        return lookup
    
    def cast(self):
        """Cast an object to its actual class."""
        subclass_obj = self
        subclasses = self.__class__.get_subclasses()
        for subclass in subclasses :
            try :
                subclass_obj = getattr(self, subclass.__name__.lower())
            except :
                continue
            else :
                subclass_obj = subclass_obj.cast()
        return subclass_obj
    
    @property
    def get_type(self):
        """Return the verbose name of the object actual class."""
        return self.cast()._meta.verbose_name
    
    @classmethod
    def subclasses_dict(cls, proxies=False):
        """Return a dictionary linking a subclass name to the actual Python subclass."""
        classes = SortedDict()
        for subclass in cls.get_subclasses(proxies) :
            classes[subclass.__name__.lower()] = subclass
        return classes
    
    class Meta :
        abstract = True

class HierarchicalStructure(models.Model):
    """
    A convenient class to manage classes corresponding to hierarchical structures, 
    i.e. classes that have a ForeignKey pointing to itself.
    """
    
    def _parents(self, field):
        """Get the parent chain."""
        result = list()
        parent = getattr(self, field.name)
        if parent :
            result.append(parent)
            result.extend(parent._parents(field))
        return result
            
    def _root(self, field):
        """Get the root node of the hierarchy."""
        root = self
        parent = getattr(root, field.name)
        while parent :
            root = parent
            parent = getattr(root, field.name)
        return root 
    
    def _children(self, field, children=None, recursive=False, starting_point=True, as_queryset=False):
        """Get recursively all children of a node."""
        if starting_point :
            children = list()
        manager = getattr(self, field.related.get_accessor_name())
        new_children = [k for k in manager.all()]
        for child in new_children :
            if not (child in children) :
                children.append(child)
            if recursive : 
                child._children(field, children, recursive, False)
        if starting_point :
            if not as_queryset :
                return children
            else :
                pks = [k.pk for k in children]
                queryset = get_base_class(self.__class__).objects.filter(pk__in=pks)
                return queryset
    
    @classmethod
    def _field(cls, forward=True):
        """Get the self referential field."""   
        related_cls = 'RelatedObject' if forward else 'ForeignKey'
        names = cls._meta.get_all_field_names()
        for name in names :
            _field = cls._meta.get_field_by_name(name)[0]
            if _field.__class__.__name__ == related_cls :
                field = _field if not forward else _field.field
                model = field.rel.to if not forward else field.related.model
                if issubclass(cls, model) :
                    return field
        raise Exception('cannot find the self referential field')
    
    def get_parents(self):
        """Get parents chain of the node."""
        field = self._field()
        return self._parents(field)
        
    def get_root(self):
        """Get the root node of the hierarchy."""
        field = self._field()
        return self._root(field)
    
    def get_children(self, recursive=False, as_queryset=False):
        """Get children of a node."""
        field = self._field(False)
        return self._children(field, recursive=recursive, as_queryset=as_queryset)
    
    class Meta :
        abstract = True

class IndexQuerySet(models.query.QuerySet):
    """
    A subclass of :class:`QuerySet` to unregister a set
    of :class:`ObjectIndex` instances from database.
    """
    
    def unregister(self):
        """Remove from database a set of :class:`ObjectIndex`."""
        for index in self._clone() :
            index.delete()

class IndexManager(models.Manager):
    """Manage the lifecycle of :class:`ObjectIndex` instances."""
    
    def get_queryset(self):
        """Return a :class:`CTOQuerySet`."""
        return IndexQuerySet(self.model, using=self._db)
    
    def _get_ct_and_index(self, obj):
        """
        Get :class:`ContentType` object and
        :class:`ObjectIndex` class relative to an object.
        """
        cls = obj.__class__
        pk_type = get_pk_type(cls)
        if issubclass(pk_type, int) :
            index = IntegerObjectIndex
        elif issubclass(pk_type, basestring) :
            index = CharObjectIndex
        else :
            raise NotImplementedError()
        ct = ContentType.objects.get_for_model(cls)
        return ct, index

    def register_object(self, obj):
        """Register a new :class:`ObjectIndex`."""
        ct, index = self._get_ct_and_index(obj)
        return index.objects.get_or_create(content_type=ct, object_id=obj.pk)[0]
    
    def register_objects(self, objects):
        """Register a new set of :class:`ObjectIndex`."""
        return [self.register_object(k) for k in objects]
    
    def get_registered_object(self, obj):
        """Get the :class:`ObjectIndex` relative to an object."""
        ct, index = self._get_ct_and_index(obj)
        objs = index.objects.filter(content_type=ct, object_id=obj.pk)
        return objs.get() if objs else None
    
    def is_registered(self, obj):
        """Tell if an object has got its :class:`ObjectIndex` counterpart."""
        return bool(self.get_registered_object(obj))
    
    def unregister_object(self, obj):
        """Remove the :class:`ObjectIndex` relative to an object from the database."""
        index = self.get_registered_object(obj)
        if index :
            index.delete()

class ObjectIndex(Cast):
    """
    An index of objects stored into the database.
    By this way it is possible to make things more
    generic. For example, annotation and permission
    systems use this index because it should be
    possible to annotate or assign a permission on
    all types of objects.
    
    NB : It is a way to replace Django's generic foreign
    keys system and its limitations on the type of the
    primary key, i.e. it should not be dependent on the
    fact that a primary key is integer or char. The system
    can manage the type of the primary key in a transparent
    manner thanks to the :class:`IntegerObjectIndex` and
    :class:`CharObjectIndex` subclasses. 
    """
    content_type = models.ForeignKey(ContentType) 
    objects = IndexManager()
    
    def __unicode__(self):
        return "%s : %s" % (self.content_type, self.cast().object)
    
class IntegerObjectIndex(ObjectIndex):
    """Index of objects having integer as primary key."""
    object_id = models.IntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    
    class Meta :
        ordering = ['content_type__model', 'object_id']

class CharObjectIndex(ObjectIndex):
    """Index of objects having text as primary key."""
    object_id = models.TextField()
    object = GenericForeignKey('content_type', 'object_id')
    
    class Meta :
        ordering = ['content_type__model', 'object_id']

def unregister_object(sender, **kwargs):
    """Unregister a :class:`ObjectIndex` right after its relative object deletion."""
    ObjectIndex.objects.unregister_object(kwargs['instance'])

#signals.post_delete.connect(unregister_object)

def unregister_referenced_index(sender, **kwargs):
    """Unregister a :class:`ObjectIndex` if there isn't any references to it."""
    instance = kwargs['instance']
    
    #get the key referencing the ObjectIndex class
    fkeys = foreign_keys(instance.__class__)
    fkeys.update(many_to_many_fields(instance.__class__))
    index_key = None
    for key, details in fkeys.items() :
        if issubclass(details['class'], ObjectIndex) :
            index_key = key
            break
    
    #if found get the ObjectIndex instance
    #its reverse foreign keys and reverse many to many fields
    #then detect if some relationships remain
    #and finally delete the ObjectIndex instance
    #if it is not the case
    if index_key :
        index = getattr(instance, index_key)
        keys = reverse_foreign_keys(ObjectIndex).keys()
        keys.extend(reverse_many_to_many_fields(ObjectIndex).keys())
        for key in keys :
            count = getattr(index, key).all()
            if count :
                return
        index.delete()
               
#signals.post_delete.connect(unregister_referenced_index)
