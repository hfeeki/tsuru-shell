#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import functools
from functools import wraps
import warnings
from configs import TOKEN_FN


def readToken(fn=TOKEN_FN):
    token = open(fn).read().strip()
    return token

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

    #check_login.__doc__ = func.__doc__
    #check_login.__name__ = func.__name__
    return check_login

def minargs_check(args, minargs):
    x = args.split()
    if len(x) < minargs:
        print("Invalid number of arguments.")
        return
    return x    


def minargs_required(minnum):
    '''
    This decorator just works for cmd derived classes.
    used to check argument string .
    '''    
    def make_wrapper(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):            
            x = args[0].split()
            if len(x) < minnum:
                print("Invalid number of arguments.")
                return 
            else:
                self.argx = x
                return f(self, *args, **kwargs)

        return wrapper

    return make_wrapper    


def require(arg_name, *allowed_types):
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


def deprecated(func):
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
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func



