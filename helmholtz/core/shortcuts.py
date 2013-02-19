#encoding:utf-8
import os
from re import search
from fnmatch import fnmatch
from django.contrib.contenttypes.models import ContentType   
    
def get_subclasses(cls, proxies=False):
    """
    Return the subclasses corresponding to
    the specified class even if it is a proxy.
    """
    if proxies :
        return cls.__subclasses__()
    else :
        return [k for k in cls.__subclasses__() if (k._meta.proxy == False)]

def generic_filter(entity, obj, ct_field, fk_field):
    """Returns the permissions relative to a specified object"""
    content_type = ContentType.objects.get_for_model(obj)
    kwargs = {ct_field + '__pk':content_type.id, fk_field:obj.id}
    queryset = entity.objects.filter(**kwargs)
    return queryset 

def cast_object_to_leaf_class(obj):
    """Cast an object to its actual class."""
    subclasses = get_subclasses(obj.__class__)
    has_got_subclass = False
    for subcls in subclasses :
        try :
            node = getattr(obj, subcls.__name__.lower())
            has_got_subclass = True
            break
        except :
            continue
    if has_got_subclass :
        return cast_object_to_leaf_class(node)
    else :
        return obj

def visit(arg, dirname, names) :
    slash = "\\" if arg[2] else "/"
    path = "%s%s" % (dirname, slash) if (dirname != '/') else dirname
    for file in names :
        if fnmatch(file.lower(), arg[0].lower()) :
            arg[1].append(path + file)

def find_file(folder='/', pattern='*') :
    """
    Find the list of files stored into the specified
    folder and corresponding to the specified pattern.
    """
    paths = []
    # correct bad slashing
    antislash = bool(os.path.splitdrive(folder)[0])
    if antislash :
        _folder = folder.replace('/', '\\')
    else :
        _folder = folder.replace('\\', '/')
    args = [pattern, paths, antislash]
    os.path.walk(_folder, visit, args)
    return paths

def get_class(application, model_name):
    """
    Get the :class:`Model` corresponding to
    the specified app name and model name.
    """
    ct = ContentType.objects.get(app_label=application, model=model_name.lower())
    return ct.model_class()

def one_help_text_at_least(form):
    """
    Return a boolean telling if a form
    contains fields having an help_text.
    """
    for field in form :
        if field.help_text :
            return True
    return False

def get_form_context(request, form, header, action=None, next_step=None):
    """Return a dictionary containing all dialog form properties."""
    context = {'form':form,
               'form_header':header,
               'cancel_redirect_to':request.session['last_page'],
               'enable_scroll_position':True,
               'action':action,
               'background_page':request.session['background_page'],
               'one_help_text_at_least':one_help_text_at_least(form),
               'next_step':next_step}
    return context

def get_by_types(obj, app, model, lookup, strict=True):
    """
    Return a list containing types corresponding
    to the specified app, model and lookup.
    """
    cls = get_class(app, model)
    objects = cls.objects.filter(**{lookup:obj}).distinct()
    subclasses = [k for k in cls.get_subclasses_recursively(strict=strict) if not k.__subclasses__()]
    retained = dict()
    for subclass in subclasses :
        casted = objects.cast(subclass)
        if casted :
            retained[subclass] = casted  
    return retained
