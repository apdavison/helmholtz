#encoding:utf-8

from django.utils.datastructures import SortedDict
from helmholtz.core.shortcuts import cast_object_to_leaf_class
from helmholtz.core.schema import many_to_many_fields
from helmholtz.core.schema import generic_relations
from helmholtz.core.schema import reverse_foreign_keys
from helmholtz.core.schema import reverse_one_to_one_keys
from helmholtz.core.schema import reverse_many_to_many_fields

"""This modules provides facilities to detect dependencies between database objects."""

def get_dependencies(cls):
    """
    Get fields materialising dependencies between 2
    classes that could lead to a delete cascading.
    """
    dct = SortedDict()
    dct.update(reverse_foreign_keys(cls))
    dct.update(reverse_one_to_one_keys(cls))
    dct.update(generic_relations(cls))
    return dct  

def get_links(cls):
    """
    Get fields materialising dependencies between 2
    classes that don't lead to a delete cascading.
    """
    dct = SortedDict()
    dct.update(many_to_many_fields(cls))
    dct.update(reverse_many_to_many_fields(cls))
    return dct

def get_all_dependencies(main_object, all_dependencies=None, level=0, starting_point=True, recursive=True):
    """
    Get recursively all objects which life
    cycle is depending on the specified object.
    """
    
    if starting_point :
        all_dependencies = list() 
    
    fields = get_dependencies(main_object.__class__)

    for name, field in fields.items() :
        lst = list()
        cast = cast_object_to_leaf_class(main_object)
        if (field['type'] != 'reverse_o2o'):
            link = getattr(cast, name)
            all = link.all()
            lst.extend(list([cast_object_to_leaf_class(k) for k in all]))
        else :
            try :
                link = getattr(cast, name)
                lst.append(link)
            except :
                pass  
        
        objects = [(k.__class__.__name__, k, field['is_required'], 20 * level) for k in lst] 
        
        if recursive and not field['type'] in ['m2m', 'reverse_m2m'] :
            for item in objects :
                all_dependencies.append(item)
                child_object = cast_object_to_leaf_class(item[1])
                cls = child_object.__class__
                get_all_dependencies(child_object, all_dependencies, level + 1, starting_point=False)  
        else :
            all_dependencies.extend(objects)
    
    if starting_point == True :
        return all_dependencies

def get_all_links(main_object):
    """
    Get all objects that are linked but
    not dependent to the specified object.
    """
    links = SortedDict()
    fields = get_links(main_object.__class__)
    if fields :
        for name, field in fields.items() :
            link = getattr(cast_object_to_leaf_class(main_object), name)
            objects = [cast_object_to_leaf_class(k) for k in link.all()]
            if objects :
                links[field['class'].__name__] = objects 
    return links
