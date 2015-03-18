#encoding:utf-8
import sys
import os
from copy import copy
from django.conf import settings
from django.db.models.loading import get_models
from helmholtz.core.shortcuts import find_file
from helmholtz.core.loggers import default_logger

logging = default_logger(__name__)

def get_project_applications(project_name=settings.PROJECT_NAME):
    project_modules = [k for k in settings.INSTALLED_APPS if k.startswith(project_name)] 
    return [k.split('.')[1] for k in project_modules]

def get_project_modules(project_name=settings.PROJECT_NAME):
    return [k for k in settings.INSTALLED_APPS if k.startswith(project_name)]

def get_foreign_modules(project_name=settings.PROJECT_NAME):
    return [k for k in settings.INSTALLED_APPS if not k.startswith(project_name)]

def is_included(module, include):
    return (not include) or (len([k for k in include if module.startswith(k)]) > 0)    

def is_excluded(module, exclude):
    return (len([k for k in exclude if module.startswith(k)]) > 0)

def filter_condition(module, include, exclude): 
    return (is_included(module, include) and not is_excluded(module, exclude))

def class_is_included(cls, include): 
    return (not include) or ("%s.%s" % (cls.__module__ , cls.__name__) in include) # 
    #return ((not bool(include)) or (len([k for k in include if ("%s.%s"%(cls.__module__ ,cls.__name__) == k)]) > 0)) 

def class_is_excluded(cls, exclude): 
    return ("%s.%s" % (cls.__module__ , cls.__name__) in exclude)
    #return (len([k for k in exclude if ("%s.%s"%(cls.__module__ ,cls.__name__) == k)]) > 0) 

def class_filter_condition(cls, include, exclude):
    return (class_is_included(cls, include) and not class_is_excluded(cls, exclude))

def physical_type(module_name):
    pass

def get_modules(module_name, modules_filter=None, chain=False, django=True):
    """Get all subpackages contained in the specified package.
    
    - modules_filter : 
    
        A convenient way to select modules. For example init modules_filter with this list [module1,module2,-module3]
        will select only module1, module2 but not module3 if it is a subpackage of one of the two preeceeding modules.
    
    """
    exec("import %s" % module_name)
    mod = sys.modules[module_name]
    if hasattr(mod, '__path__') :
        #get all python files
        location = mod.__path__[0]
        extension = "py"
        pattern = "*.%s" % (extension)
        files = [k for k in find_file(location, pattern)]
        
    else :
        extension = "pyc"
        file = mod.__file__
        files = [file]
    #keep only module names from paths
    all_modules = list()
    for file in files :
        ignore = len(extension) + 1
        name = file.replace('/', '.').replace('\\', '.')[:-ignore]
        index = name.index(module_name)
        all_modules.append(name[index:])
    
    #initialize module filter
    filter = list()
    if isinstance(modules_filter, list) :
        filter.extend(modules_filter)
    #compute include and exclude from modules_filter
    #filter selected modules
    include = set([k for k in filter if not k.startswith('-')])
    include.add(module_name)
    exclude = set([k[1:] for k in filter if k.startswith('-')])    
    module_names = [k for k in all_modules if filter_condition(k, include, exclude) and (not django or ('models' in k))]
    #store modules relative to files
    modules = list()
    for name in module_names :
        __import__(name)
        modules.append(sys.modules[name])
    #modules.sort(key=lambda x:x.__name__)   
    if chain :
        return modules, include, exclude 
    else :
        return modules

def get_dependency_chain(entity, strict=False):
    all_dependencies = list()
    #get dependencies at the entity level
    fkeys = [k for k in entity._meta.local_fields if (k.__class__.__name__ == 'ForeignKey')]
    m2m = [k for k in entity._meta.local_many_to_many if (k.__class__.__name__ != 'GenericRelation')]
    keys = list()
    keys.extend(fkeys)
    keys.extend(m2m)
    dependencies = [k.rel.to for k in keys]
    #make the recursion
    for dependency in dependencies :
        if dependency != entity :
            all_dependencies.append(dependency)
            all_dependencies.extend(get_dependency_chain(dependency, True))
    if not strict :
        all_dependencies.insert(0, entity)
    return all_dependencies
    
def dir_module(module_name, modules_filter=None, classes_filter=None, recursive=True, only_model=True, django=True, proxies=True, abstract=True, select_foreign_models=False, all_classes=None, cls_include=None, cls_exclude=None, starting_point=True):
    """Get all classes contained in the specified package and corresponding to database models.
    
    - modules_filter : 
    
        A convenient way to select modules. For example init modules_filter with this list [module1,module2,-module3]
        will select only module1, module2 but not module3 if it is a subpackage of one of the two preeceeding modules.
    
    - classes_filter :
    
        ...
    
    - recursive : Enables recursion into subpackages.
    
    """
    #initial conditions
    if starting_point :
        all_classes = set()
        filter = list()
        if isinstance(classes_filter, list) :
            filter.extend(classes_filter)
        cls_include = set([k for k in filter if not k.startswith('-')])
        cls_exclude = set([k[1:] for k in filter if k.startswith('-')])
    #when the process reach a database models
    #it is added to the all_classes parameter
    #if the reached class is not contained in 
    #the specified module and if recursive is True,
    #the process will go into the foreign module
    #containing the class      
    modules, include, exclude = get_modules(module_name, modules_filter, True, django)
    for module in modules :
        for item in dir(module) :
            member = getattr(module, item)
            attributes = dir(member)        
            if isinstance(member, type) :
                is_internal_module = (member.__module__ in [k.__name__ for k in modules])
                if (not only_model or (member.__class__.__name__ == 'ModelBase')) \
                    and ((not is_internal_module and select_foreign_models) or filter_condition(member.__module__, include, exclude)) \
                    and class_filter_condition(member, cls_include, cls_exclude) \
                    and not ('_meta' in attributes and (member._meta.proxy or member._meta.abstract)) :
                    all_classes.add(member)
                    if recursive and not is_internal_module and select_foreign_models :
                        dependencies = set([k for k in get_dependency_chain(member) if filter_condition(k.__module__, include, exclude) and class_filter_condition(k, cls_include, cls_exclude)])
                        all_classes.update(dependencies)
                        
    #end of the recursion        
    if starting_point :
        result = list(all_classes)
        result.sort(key=lambda x:sys.modules[x.__module__].__name__)
        return result

def get_model_classes(module_name, modules_filter=None, classes_filter=None, select_foreign_models=False, select_recursive=True, recursive=True):
    """Get all classes corresponding to the packaged database model (cf get_modules and dir_modules)."""
    classes = dir_module(module_name, modules_filter, classes_filter, recursive, True, True, False, False, select_foreign_models)
    return classes                      

def get_application_classes(project_name=settings.PROJECT_NAME, modules_filter=None, classes_filter=None):
    classes = set()
    filter = list()
    if modules_filter :
        filter.extend(modules_filter)
    include = [k for k in filter if not k.startswith('-')]
    exclude = [k for k in filter if k.startswith('-')]
    
    def _is_included(module, include):
        return (not include) or (len([k for k in include if (k.startswith(module) or module.startswith(k))]) > 0)    

    def _is_excluded(module, exclude):
        return (len([k for k in exclude if (k.startswith(module) or module.startswith(k))]) > 0)

    def _filter_condition(module, include, exclude):
        return (_is_included(module, include) and not _is_excluded(module, exclude))

    applications = [k for k in settings.INSTALLED_APPS if _filter_condition(k, include, exclude)]
    applications.reverse()
    for application in applications :
        app_classes = get_model_classes(application, modules_filter=filter, classes_filter=classes_filter)
        classes.update(app_classes)
    result = list(classes)
    result.sort(key=lambda x:x.__module__)
    return result

def get_model_class(module_name, class_name):
    classes = get_model_classes(module_name)
    class_dct = {}
    for cls in classes :
        class_dct[cls.__name__] = cls
    assert class_dct.has_key(class_name), "module %s does not contain class %s" % (module_name, class_name)
    return class_dct[class_name]

application_classes = get_models()#get_application_classes()

if __name__ == '__main__' :
    classes = 0
    #classes = dir_module('brainscales_db.analysis')
    #assert len(classes) == 25
    #classes = dir_module('brainscales_db.annotation')
    #assert len(classes) == 14
    #classes = dir_module('brainscales_db.chemistry')
    #assert len(classes) == 4
    #classes = dir_module('brainscales_db.drug_applications')
    #assert len(classes) == 3
    #classes = dir_module('brainscales_db.electricalstimulation')
    #assert len(classes) == 1
    #classes = dir_module('brainscales_db.electrophysiology')
    #assert len(classes) == 20
    #classes = dir_module('brainscales_db.equipment')
    #assert len(classes) == 9
    #classes = dir_module('brainscales_db.experiment')
    #assert len(classes) == 1
    #classes = dir_module('brainscales_db.histochemistry')
    #assert len(classes) == 3
    #classes = dir_module('brainscales_db.location')
    #assert len(classes) == 2
    #classes = dir_module('brainscales_db.measurements')
    #assert len(classes) == 8
    #classes = dir_module('brainscales_db.neuralstructures')
    #assert len(classes) == 4
    #classes = dir_module('brainscales_db.optical_imaging')
    #assert len(classes) == 6
    #classes = dir_module('brainscales_db.people')
    #assert len(classes) == 11
    #classes = dir_module('brainscales_db.preparations')
    #assert len(classes) == 9
    #classes = dir_module('brainscales_db.reconstruction')
    #assert len(classes) == 1
    #classes = dir_module('brainscales_db.recording')
    #assert len(classes) == 4
    #classes = dir_module('brainscales_db.signals')
    #assert len(classes) == 4
    #classes = dir_module('brainscales_db.species')
    #assert len(classes) == 2
    #classes = dir_module('brainscales_db.stimulation')
    #assert len(classes) == 1
    #classes = dir_module('brainscales_db.storage')
    #assert len(classes) == 5
    #classes = dir_module('brainscales_db.units')
    #assert len(classes) == 2
    #classes = dir_module('brainscales_db.visualstimulation')
    #assert len(classes) == 4
    #classes = dir_module('brainscales_db.waveforms')
    #assert len(classes) == 3
    #classes = dir_module('brainscales_db')
    #assert len(classes) == 161
    #cls = get_application_classes()

