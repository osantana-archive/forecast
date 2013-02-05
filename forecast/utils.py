# coding: utf-8


import imp
import os


MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')


def import_object(name):
    module_path, object_name = name.rsplit(".", 1)

    try:
        module = __import__(module_path, fromlist=[object_name])
    except ImportError, ex:
        raise ImportError("%s (%s)" % (ex, module_path))

    try:
        object = getattr(module, object_name)
    except AttributeError:
        raise ImportError("No symbol named %s on module %s" % (object_name, module_path))

    return module, object


def package_contents(package_name, filter=None):
    parts = package_name.split(".")
    pathname = None
    for part in parts:
        if pathname:
            pathname = [pathname]
        file, pathname, description = imp.find_module(part, pathname)
        if file:
            raise ImportError('Not a package: %r', package_name)

    ret = set()
    for module in os.listdir(pathname):
        modname = os.path.splitext(module)[0]

        if filter and filter(modname):
            continue

        if module.endswith(MODULE_EXTENSIONS):
            ret.add(modname)

    return ret


def camelize(name):
    parts = [ part.title() for part in name.split("_") if part ]
    return "".join(parts)
