# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:value_dispatch.py
@time:2021/12/16
"""
import functools


def value_dispatch(func):
    """
    Like singledispatch() but dispatches by value of the first arg.
    """

    registry = {}

    @functools.wraps(func)
    def wrapper(arg0, *args, **kwargs):
        try:
            delegate = registry[arg0]
        except KeyError:
            pass
        else:
            return delegate(arg0, *args, **kwargs)

        return func(arg0, *args, **kwargs)

    def register(value):
        def wrap(func):
            if value in registry:
                raise ValueError(
                    f'@value_dispatch: there is already a handler '
                    f'registered for {value!r}'
                )
            registry[value] = func
            return func
        return wrap

    def register_for_all(values):
        def wrap(func):
            for value in values:
                if value in registry:
                    raise ValueError(
                        f'@value_dispatch: there is already a handler '
                        f'registered for {value!r}'
                    )
                registry[value] = func
            return func
        return wrap

    wrapper.register = register
    wrapper.register_for_all = register_for_all
    return wrapper
