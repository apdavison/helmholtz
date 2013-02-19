#encoding:utf-8

# functions operating on core models and auxiliary classes

from django.utils.datastructures import SortedDict
from django.db.models import ForeignKey
from django.db.models import OneToOneField
from django.db.models import ManyToManyField
from django.db.models import AutoField
from django.db.models import IntegerField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models.related import RelatedObject
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.contenttypes.generic import GenericForeignKey
from helmholtz.core.shortcuts import get_subclasses

def get_parents_recursively(entity):
    """Return parent classes defining a hierarchy of subclass."""
    result = list()
    for parent in entity._meta.parents :
        result.append(parent)
        result.extend(get_parents_recursively(parent))
    return result

def create_subclass_lookup(entity, base_class=None):
    """Get the entire lookup from the base class to the target subclass."""
    parents = entity.get_parents_recursively()
    index = -1 if not base_class else parents.index(base_class)
    chain = parents[0:index]
    chain.reverse()
    chain.append(entity)
    lookup = '__'.join([k.__name__.lower() for k in chain])
    return lookup

def regular_fields(entity, inheritance=False):
    """Return regular fields of the specified :class:`Model`."""
    choices = ['ForeignKey', 'OneToOneField']
    fields = [k.name for k in entity._meta.fields if not (k.__class__.__name__ in choices)] 
    return fields 

def is_regular_field(entity, field):
    """Return a boolean telling if a field is a regular field."""
    fields = regular_fields(entity)
    return (field in fields)

def subclasses(entity, proxies=False):
    """Return all direct subclasses of the specified :class:`Model`."""
    classes = SortedDict()
    for subclass in get_subclasses(entity, proxies) :
        classes[subclass.__name__.lower()] = subclass
    return classes

def get_subclasses_recursively(entity, strict=True, proxies=False, excluded_subclasses=[]):
    """Return all subclasses of a :class:`Model` in a recursive manner."""
    subclasses = list()
    for subclass in get_subclasses(entity, proxies) :
        if not subclass in excluded_subclasses :
            subclasses.append(subclass)
            subclasses.extend(get_subclasses_recursively(subclass))
    if not strict and (not entity in excluded_subclasses) :
        subclasses.insert(0, entity)    
    return subclasses

def get_base_class(entity):
    """Return the root base class of a :class:`Model`."""
    parents = get_parents_recursively(entity) 
    return parents[-1] if parents else entity

def cast_queryset(queryset, key):
    """Return a :class:`QuerySet` filtered by actual object type."""
    subclasses = get_subclasses_recursively(queryset.model)
    if isinstance(key, str) :
        names = [k.__name__ for k in subclasses]
        index = names.index(key)
    else :
        index = subclasses.index(key)
    selection = subclasses[index]
    lookup = create_subclass_lookup(selection)
    dct = {'%s__isnull' % lookup:False}
    pks = [k.id for k in queryset.filter(**dct).distinct()]
    objects = selection.objects.filter(pk__in=pks)
    return objects

def self_referential_field(cls, forward=True):
    """Return the field that is a self referential one."""
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

def get_parent_chain(obj, _field=None):
    """Return all node of a hierarchy defined by a self referencing :class:`Model`.""" 
    result = list()
    field = self_referential_field(obj.__class__) if not _field else _field
    parent = getattr(obj, field.name)
    if parent :
        result.append(parent)
        result.extend(get_parent_chain(parent, field))
    return result
        
def get_root_node(obj, _field=None):
    """Return the root node of a hierarchy defined by a self referencing :class:`Model`."""
    field = self_referential_field(obj.__class__) if not _field else _field
    parent = getattr(obj, field.name)
    if parent :
        return get_root_node(parent, field)
    else :
        return obj

def get_all_children(obj, _field=None, children=None, recursive=False, starting_point=True, as_queryset=False):
    """Return children of the specified object in a recursive manner."""
    if starting_point :
        children = list()
    field = self_referential_field(obj.__class__, False) if not _field else _field
    manager = getattr(obj, field.get_accessor_name())
    new_children = [k for k in manager.all()]
    for child in new_children :
        if not (child in children) :
            children.append(child)
        if recursive : 
            get_all_children(child, field, children, recursive, False)
    if starting_point :
        if not as_queryset :
            return children
        else :
            pks = [k.pk for k in children]
            queryset = obj.__class__.objects.filter(pk__in=pks)
            return queryset

def subclasses_tree(entity):
    """Return subclasses of the specified :class:`Model` in a recursive manner."""
    classes = SortedDict()
    for subclass in entity.__subclasses__() :
        class_name = subclass.__name__.lower()
        classes[class_name] = SortedDict()
        classes[class_name]['class'] = subclass
        classes[class_name]['field'] = subclass._meta.pk.name
    return classes

def foreign_keys(entity, display_ptr=True):
    """Return foreign keys instances of a of :class:`Model`."""
    choices = ['ForeignKey', 'OneToOneField']
    fks = SortedDict()
    entities = get_parents_recursively(entity)
    entities.reverse()
    entities.append(entity)
    for entity in entities :
        for field in entity._meta.fields :
            if (field.__class__.__name__ in choices) :
                strict = (entity.__class__.__name__ != field.rel.to.__class__.__name__) 
                is_strict_subclass = (display_ptr and issubclass(entity, field.rel.to) and strict)
                if (not is_strict_subclass) : 
                    fks[field.name] = SortedDict()
                    fks[field.name]['verbose_name'] = field.verbose_name
                    fks[field.name]['class'] = field.rel.to
                    fks[field.name]['field'] = field.rel.field_name  
                    fks[field.name]['is_required'] = not field.null
                    fks[field.name]['type'] = 'o2o' if (field.__class__.__name__ != 'ForeignKey') else 'fk' 
#                    fks[field.name]['is_o2o'] = True if (field.__class__.__name__ != 'ForeignKey') else False
    return fks 

def many_to_many_fields(entity):
    """Return local many to many fields of a :class:`Model`."""
    mks = SortedDict()
    entities = get_parents_recursively(entity)
    entities.reverse()
    entities.append(entity)
    for entity in entities :
        for field in entity._meta.local_many_to_many :
            if field.__class__.__name__ != 'GenericRelation' :
                mks[field.name] = SortedDict()
                mks[field.name]['class'] = field.rel.to
                mks[field.name]['field'] = field.rel.get_related_field().name    
                mks[field.name]['type'] = 'm2m'
                mks[field.name]['is_required'] = False #not field.null
    return mks

def reverse_one_to_one_keys(entity):
    """Return reverse one to one fields of a :class:`Model`."""
    fks = foreign_keys(entity)
    reverse_oks = SortedDict()
    choices = ['ReverseSingleRelatedObjectDescriptor', 'SingleRelatedObjectDescriptor']
    internal = entity.__dict__
    for field in internal :
        attribute = internal[field]
        class_name = attribute.__class__.__name__
        if (not (field in fks)) and (class_name in choices) :
            subcls = entity.__subclasses__()
            if (class_name == choices[0]) and not (attribute.field.rel.to in subcls) :
                reverse_oks[field] = SortedDict()
                reverse_oks[field]['class'] = attribute.field.rel.to
                reverse_oks[field]['field'] = attribute.field.rel.field_name
                f = getattr(attribute.field.rel.to, attribute.field.rel.field_name)
                reverse_oks[field]['is_required'] = not f.null
                reverse_oks[field]['type'] = 'reverse_o2o'
            elif class_name == choices[1] and not (attribute.related.model in subcls) :
                reverse_oks[field] = SortedDict() 
                reverse_oks[field]['class'] = attribute.related.model
                reverse_oks[field]['field'] = attribute.related.field.name
                reverse_oks[field]['is_required'] = not attribute.related.field.null
                reverse_oks[field]['type'] = 'reverse_o2o'
    return reverse_oks

def reverse_foreign_keys(entity):
    """Return reverse reverse foreign keys of a :class:`Model`."""
    fks = foreign_keys(entity)
    reverse_fks = SortedDict()
    choices = ['ForeignRelatedObjectsDescriptor']
    all_classes = list(entity._meta.get_parent_list())
    all_classes.append(entity)
    for cls in all_classes :
        internal = cls.__dict__
        for field in internal :
            attribute = internal[field]
            class_name = attribute.__class__.__name__
            if (not (field in fks)) and (class_name in choices) and not (class_name in reverse_fks) :
                if class_name == choices[0] : 
                    reverse_fks[field] = SortedDict()
                    reverse_fks[field]['class'] = attribute.related.model
                    reverse_fks[field]['field'] = attribute.related.field.name
                    reverse_fks[field]['is_required'] = not attribute.related.field.null
                    reverse_fks[field]['type'] = 'reverse_fk'
    return reverse_fks

def reverse_many_to_many_fields(entity):
    """Return reverse many to many fields of a :class:`Model`."""
    mks = many_to_many_fields(entity)
    reverse_mks = SortedDict()
    internal = entity.__dict__
    for field in internal :
        attribute = internal[field]
        class_name = attribute.__class__.__name__
        if (not (field in mks)) and (class_name == "ManyRelatedObjectsDescriptor") :
            reverse_mks[field] = SortedDict()
            reverse_mks[field]['class'] = attribute.related.model
            reverse_mks[field]['field'] = attribute.related.field.name
            reverse_mks[field]['is_required'] = False
            reverse_mks[field]['type'] = 'reverse_m2m'
    return reverse_mks

def generic_foreign_keys(entity):
    """Return local generic foreign keys of a :class:`Model`."""
    gfks = SortedDict()
    for attr in entity._meta.virtual_fields :
        if attr.__class__.__name__ == 'GenericForeignKey' :
            gfks[attr.name] = SortedDict()
            gfks[attr.name]['ct_field'] = attr.ct_field
            gfks[attr.name]['fk_field'] = attr.fk_field  
            gfks[attr.name]['type'] = 'generic_fk' 
            gfks[attr.name]['is_required'] = True
    return gfks

def generic_relations(entity):
    """Return local generic relations of a :class:`Model`."""
    grs = SortedDict()
    entities = get_parents_recursively(entity)
    entities.reverse()
    entities.append(entity)
    for entity in entities :
        for field in entity._meta.local_many_to_many :
            if field.__class__.__name__ == 'GenericRelation' :
                gfk = [k.name for k in field.rel.to._meta.virtual_fields if (k.__class__.__name__ == 'GenericForeignKey') and (k.ct_field == field.content_type_field_name) and (k.fk_field == field.object_id_field_name)]
                assert len(gfk) == 1, "problem with GenericRelation key of model %s" % (entity)
                grs[field.name] = SortedDict()
                grs[field.name]['class'] = field.rel.to
                grs[field.name]['verbose'] = field.verbose_name
                grs[field.name]['field'] = gfk[0] 
                grs[field.name]['type'] = 'generic_rel' 
                grs[field.name]['is_required'] = True
    return grs

"""
The following Field, Property, GenericFKey and Link classes
are convenient way to encapsulate field data, and select only
of those are useful in the scope of Helmholtz, into a python object.
"""

class Field(object):
    
    def __init__(self, klass, name, verbose_name):
        self.klass = klass
        self.name = name
        self.verbose_name = verbose_name
    
    def __repr__(self):
        return "(%s,%s)" % (self.klass, self.name)

class Property(Field):
    pass

class GenericFKey(Field):
    
    def __init__(self, klass, name, ct_field, fk_field):
        super(GenericFKey, self).__init__(klass, name, name)
        self.ct_field = ct_field
        self.fk_field = fk_field
    
    def __repr__(self):
        return "(%s,%s,%s,%s)" % (self.klass, self.name, self.ct_field, self.fk_field)

class Link(object):
    
    def __init__(self, source, destination, type, reverse, required):
        self.source = source
        self.destination = destination
        self.required = required #tells if the field is required in the source class
        self.reverse = reverse #tells if it is a reverse link
        self.type = type
        if reverse :
            self.name = getattr(destination, 'name', None)
            self.verbose_name = getattr(destination, 'verbose_name', None)
            self.klass = getattr(source, 'klass', None)
        else :
            self.name = getattr(source, 'name', None)
            self.verbose_name = getattr(source, 'verbose_name', None)
            self.klass = getattr(destination, 'klass', None)
    
    def __repr__(self):
        return "%s from %s to %s" % (self.type, self.source, self.destination)

def get_all_fields(entity, excluded_fields=[]):
    """Return all fields relative to a :class:`Model`."""
    fields = [entity._meta.get_field_by_name(k)[0] for k in entity._meta.get_all_field_names()]
    fields = [k for k in fields if not (k.name in excluded_fields) or not (k.get_accessor_name() in excluded_fields)]
    fields.extend([k for k in entity._meta.virtual_fields if not k.name in excluded_fields])
    return fields 

def reverse_objects(entity, field_type, rel_code, excluded_fields=[]):
    """Return reverse fields of a :class:`Model` of a specified type."""
    dct = SortedDict()
    rels = [k for k in get_all_fields(entity) if isinstance(k, RelatedObject) and (k.field.__class__.__name__ == field_type) and (not k.get_accessor_name() in excluded_fields)]
    models = [k.field.model for k in rels]
    for rel in rels :
        accessor_name = rel.get_accessor_name()
        source = Field(rel.field.model, rel.field.name, rel.field.verbose_name) 
        verbose_name = rel.field.model._meta.verbose_name if rel_code == 'reverse_o2o' else rel.field.model._meta.verbose_name_plural
        if models.count(rel.field.model) > 1 :
            verbose_name = '%s (%s)' % (verbose_name, rel.field.name)
        destination = Field(entity, accessor_name, verbose_name)
        dct[accessor_name] = Link(source, destination, rel_code, True, not rel.field.null if (rel_code != 'reverse_m2m') else False)
    return dct

class FieldFactory(object):   
    """
    A convenient factory class that detect all
    fields relative to a :class:`Model`and a 
    dictionary associating field names to
    :class:`Field` or :class:`Link` objects.
    """
    
    def _fkey(self, entity, field, result):
        strict = (entity.__class__.__name__ != field.rel.to.__class__.__name__) 
        is_strict_subclass = issubclass(entity, field.rel.to) and strict
        if (not is_strict_subclass) : 
            dfield = field.rel.get_related_field()
            source = Field(entity, field.name, field.verbose_name)
            destination = Field(dfield.model, dfield.name, dfield.verbose_name)
            tp = 'o2o' if (field.__class__.__name__ != 'ForeignKey') else 'fk'
            result[field.name] = Link(source, destination, tp, False, not field.null)

    def _m2m(self, entity, field, result):
        dfield = field.rel.get_related_field()
        source = Field(entity, field.name, field.verbose_name)
        destination = Field(dfield.model, dfield.name, dfield.verbose_name)
        result[field.name] = Link(source, destination, 'm2m', False, False)
    
    def _grel(self, entity, field, result):
        dfield = field.rel.get_related_field()
        source = Field(entity, field.name, field.verbose_name)
        destination = Field(dfield.model, dfield.name, dfield.verbose_name)
        result[field.name] = Link(source, destination, 'generic_rel', False, False)
    
    def _gfkey(self, entity, field, result):
        source = GenericFKey(entity, field.name, field.ct_field, field.fk_field)
        result[field.name] = Link(source, None, 'generic_fk', False, not field.ct_field.null)
    
    def _field(self, entity, field, result):
        result[field.name] = Field(entity, field.name, field.verbose_name)

    def _reverse(self, entity, related, code, result):
        accessor_name = related.get_accessor_name()
        source = Field(related.field.model, related.field.name, related.field.verbose_name)
        destination = Field(entity, accessor_name, related.field.model._meta.verbose_name if code == 'reverse_o2o' else related.field.model._meta.verbose_name_plural)
        result[accessor_name] = Link(source, destination, code, True, not related.field.null if (code != 'reverse_m2m') else False)

    def create(self, entity, excluded_fields=[]):
        result = SortedDict()
        fields = get_all_fields(entity, excluded_fields)
        for field in fields :
            if isinstance(field, (ForeignKey, OneToOneField)) :
                self._fkey(entity, field, result)    
            elif isinstance(field, ManyToManyField) :
                self._m2m(entity, field, result)
            elif isinstance(field, GenericRelation) :
                self._grel(entity, field, result)
            elif isinstance(field, GenericForeignKey) :
                self._gfkeys(entity, field, result)
            elif isinstance(field, RelatedObject) :
                if field.field.__class__.__name__ == 'ForeignKey' :
                    self._reverse(entity, field, 'reverse_fk', result)
                elif field.field.__class__.__name__ == 'OneToOneField' :
                    self._reverse(entity, field, 'reverse_o2o', result)
                elif field.field.__class__.__name__ == 'ManyToManyField' :
                    self._reverse(entity, field, 'reverse_m2m', result)
            else :
                self._field(entity, field, result)
        return result
    
def regular_fields_objects(entity, excluded_fields=[]):
    """Return regular fields of the specified :class:`Model`."""
    fields = SortedDict()
    choices = ['ForeignKey', 'OneToOneField']
    for field in entity._meta.fields :
        if not (field.name in excluded_fields) and not (field.__class__.__name__ in choices) :
            fields[field.name] = Field(entity, field.name, field.verbose_name)
    return fields 

def foreign_keys_objects(entity, excluded_fields=[], display_ptr=True):
    """Return foreign keys of a of :class:`Model`."""
    choices = ['ForeignKey', 'OneToOneField']
    fks = SortedDict()
    entities = get_parents_recursively(entity)
    entities.reverse()
    entities.append(entity)
    for entity in entities :
        for field in entity._meta.fields :
            if (field.__class__.__name__ in choices) and (not field.name in excluded_fields) :
                strict = (entity.__class__.__name__ != field.rel.to.__class__.__name__) 
                is_strict_subclass = (display_ptr and issubclass(entity, field.rel.to) and strict)
                if (not is_strict_subclass) : 
                    dfield = field.rel.get_related_field()
                    source = Field(entity, field.name, field.verbose_name)
                    destination = Field(dfield.model, dfield.name, dfield.verbose_name)
                    tp = 'o2o' if (field.__class__.__name__ != 'ForeignKey') else 'fk'
                    fks[field.name] = Link(source, destination, tp, False, not field.null)
    return fks 

def many_to_many_fields_objects(entity, excluded_fields=[]):
    """Return local many to many fields of a :class:`Model`."""
    mks = SortedDict()
    entities = get_parents_recursively(entity)
    entities.reverse()
    entities.append(entity)
    for entity in entities :
        for field in entity._meta.local_many_to_many :
            if (field.__class__.__name__ != 'GenericRelation') and (not field.name in excluded_fields) :
                dfield = field.rel.get_related_field()
                source = Field(entity, field.name, field.verbose_name)
                destination = Field(dfield.model, dfield.name, dfield.verbose_name)
                mks[field.name] = Link(source, destination, 'm2m', False, False)
    return mks

def generic_relations_objects(entity, excluded_fields=[]):
    """Return local generic relations of a :class:`Model`."""
    grs = SortedDict()
    entities = get_parents_recursively(entity)
    entities.reverse()
    entities.append(entity)
    for entity in entities :
        for field in entity._meta.local_many_to_many :
            if (field.__class__.__name__ == 'GenericRelation') and (not field.name in excluded_fields) :
                dfield = field.rel.get_related_field()
                source = Field(entity, field.name, field.verbose_name)
                destination = Field(dfield.model, dfield.name, dfield.verbose_name)
                grs[field.name] = Link(source, destination, 'generic_rel', False, True)
    return grs

def generic_foreign_keys_objects(entity, excluded_fields=[]):
    """Return local generic foreign keys of a :class:`Model`."""
    gfks = SortedDict()
    for attr in entity._meta.virtual_fields :
        if (attr.__class__.__name__ == 'GenericForeignKey') and (not attr.name in excluded_fields):
            ct_field = entity._meta.get_field_by_name(attr.ct_field)
            fk_field = entity._meta.get_field_by_name(attr.fk_field)
            assert ct_field, "bad ct_field : %s not in %s" % (attr.ct_field, entity)
            assert fk_field, "bad fk_field : %s not in %s" % (attr.fk_field, entity)
            source = GenericFKey(entity, attr.name, attr.ct_field, attr.fk_field)
            gfks[attr.name] = Link(source, None, 'generic_fk', False, True)
    return gfks

def reverse_one_to_one_keys_objects(entity, excluded_fields=[]):
    """Return reverse one to one fields of a :class:`Model`."""
    return reverse_objects(entity, 'OneToOneField', 'reverse_o2o', excluded_fields)

def reverse_foreign_keys_objects(entity, excluded_fields=[]):
    """Return reverse reverse foreign keys of a :class:`Model`."""
    return reverse_objects(entity, 'ForeignKey', 'reverse_fk', excluded_fields)

def reverse_many_to_many_fields_objects(entity, excluded_fields=[]):
    """Return reverse many to many fields of a :class:`Model`."""
    return reverse_objects(entity, 'ManyToManyField', 'reverse_m2m', excluded_fields)

def get_pk_type(cls):
    """Get the type of the primary key field of a :class:`Model`."""
    if isinstance(cls._meta.pk, AutoField) or isinstance(cls._meta.pk, IntegerField) :
        pk_type = int
    elif isinstance(cls._meta.pk, CharField) or isinstance(cls._meta.pk, TextField) :
        pk_type = basestring
    elif isinstance(cls._meta.pk, OneToOneField) :
        pk_type = get_pk_type(cls._meta.pk.related.parent_model)
    else :
        raise NotImplementedError('Cannot object with a primary key type different from AutoField, OneToOneField, IntegerField, CharField or TextField.')
    return pk_type
