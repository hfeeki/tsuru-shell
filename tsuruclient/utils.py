#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import functools
from functools import wraps
import warnings
from configs import TOKEN_FN, KEY_FN, IDENT


def readToken(fn=TOKEN_FN):
    with open(fn) as f:
        token = f.read().strip()
        return token

def readkey(fn=KEY_FN):      
    with open(fn) as f:
        c = f.read().strip()
        return c       

def login_required(func):
    @wraps(func)
    def check_login(self, *args, **kw):
        if not os.path.exists(TOKEN_FN):
            print("Please login first!\n")
            return 
        else:
            self.tk = readToken(TOKEN_FN) # stored it in self.tk
            self.auhd = {'Authorization': self.tk}
            return func(self, *args, **kw)

    return check_login

def minargs_required(minnum):
    '''
    This decorator just works for cmd derived classes.
    used to check argument string .
    '''    
    def make_wrapper(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs): 
            x = args[3].split() # third arg 
            self.argx = x
            if len(x) < minnum:
                print("Invalid number of arguments.")
                return                         
            else:                
                return f(self, *args, **kwargs)

        return wrapper

    return make_wrapper    


'''
    # http://code.activestate.com/recipes/454322-type-checking-decorator/
    @require("x", int, float)
    @require("y", float)
    def foo(x, y):
        return x+y

    print foo(1, 2.5)      # Prints 3.5.
    print foo(2.0, 2.5)    # Prints 4.5.
    print foo("asdf", 2.5) # Raises TypeError exception.
    print foo(1, 2)        # Raises TypeError exception.
'''
def require(arg_name, *allowed_types):
    
    def make_wrapper(f):
        if hasattr(f, "wrapped_args"):
            wrapped_args = getattr(f, "wrapped_args")
        else:
            code = f.func_code
            wrapped_args = list(code.co_varnames[:code.co_argcount])

        try:
            arg_index = wrapped_args.index(arg_name)
        except ValueError:
            raise NameError, arg_name

        def wrapper(*args, **kwargs):
            if len(args) > arg_index:
                arg = args[arg_index]
                if not isinstance(arg, allowed_types):
                    type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                    raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))
            else:
                if arg_name in kwargs:
                    arg = kwargs[arg_name]
                    if not isinstance(arg, allowed_types):
                        type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                        raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))

            return f(*args, **kwargs)

        wrapper.wrapped_args = wrapped_args
        return wrapper

    return make_wrapper


'''
This is a decorator which can be used to mark functions
as deprecated. It will result in a warning being emitted
when the function is used.

# === Examples of use ===

@deprecated
def some_old_function(x,y):
    return x + y

class SomeClass:
    @deprecated
    def some_old_method(self, x,y):
        return x + y  
'''
def deprecated(func):
    
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


'''
# http://code.activestate.com/recipes/408937-basic-exception-handling-idiom-using-decorators/
# ExpHandler Usage:

def myhandler(e):
    print 'Caught exception!', e
    
# Examples
# Specify exceptions in order, first one is handled first
# last one last.
@ExpHandler((ZeroDivisionError,ValueError), (None,myhandler))
def f1():
    1/0

@ExpHandler((TypeError, ValueError, StandardError), (myhandler,)*3)
def f2(*pargs, **kwargs):
    print pargs
    x = pargs[0]
    y = x[0]
    y += x[1]

@ExpHandler((ValueError, Exception))
def f3(*pargs):
    l = pargs[0]
    return l.index(10)

if __name__=="__main__":
    f1()
    # Calls exception handler
    f2('Python', 1)
    # Calls exception handler
    f3(range(5),)
'''
def ExpHandler(*posargs):

    def nestedhandler(func,exptuple, *pargs, **kwargs):
        """ Function that creates a nested exception handler from
        the passed exception tuple """

        exp, handler = exptuple[0]
        try:
            if len(exptuple)==1:
                func(*pargs, **kwargs)
            else:
                nestedhandler(func,exptuple[1:], *pargs, **kwargs)
        except exp, e:
            if handler:
                handler(e)
            else:
                print e.__class__.__name__,':',e                
        
    @wraps(f)
    def wrapper(f):
        def newfunc(*pargs, **kwargs):
            if len(posargs)<2:
                t = tuple(item for item in posargs[0] if issubclass(item,Exception) or (Exception,))
                try:
                    f(*pargs, **kwargs)
                except t, e:
                    print e.__class__.__name__,':',e
            else:
                t1, t2 =posargs[0], posargs[1]
                l=[]
                for x in xrange(len(t1)):
                    try:
                        l.append((t1[x],t2[x]))
                    except:
                        l.append((t1[x],None))

                # Reverse list so that exceptions will
                # be caught in order.
                l.reverse()
                t = tuple(l)
                nestedhandler(f,t,*pargs,**kwargs)
                    
        return newfunc

    return wrapper


