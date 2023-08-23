# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _TypeConverterModule
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class TypeConverter(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, TypeConverter, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, TypeConverter, name)
    __repr__ = _swig_repr
    def char2int(*args): return _TypeConverterModule.TypeConverter_char2int(*args)
    def int2char(*args): return _TypeConverterModule.TypeConverter_int2char(*args)
    def char2ushort(*args): return _TypeConverterModule.TypeConverter_char2ushort(*args)
    def ushort2char(*args): return _TypeConverterModule.TypeConverter_ushort2char(*args)
    def uchar2int(*args): return _TypeConverterModule.TypeConverter_uchar2int(*args)
    def int2uchar(*args): return _TypeConverterModule.TypeConverter_int2uchar(*args)
    def __init__(self, *args): 
        this = _TypeConverterModule.new_TypeConverter(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _TypeConverterModule.delete_TypeConverter
    __del__ = lambda self : None;
TypeConverter_swigregister = _TypeConverterModule.TypeConverter_swigregister
TypeConverter_swigregister(TypeConverter)



