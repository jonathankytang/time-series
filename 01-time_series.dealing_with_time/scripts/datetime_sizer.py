from __future__ import print_function
from sys import getsizeof, stderr
from itertools import chain
from collections import deque

from datetime import datetime
import numpy as np

try:
    from reprlib import repr
except ImportError:
    pass

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


##### Example call #####

if __name__ == '__main__':

    print("datetime object")
    d1 = datetime(year=2018, month=11, day=2)
    print(total_size(d1))

    print("numpy datetime64 object")
    d2 = np.datetime64('2018-10-02')
    print(total_size(d2))

    print("list of datetime objects")
    dates1 = [datetime(year=2018, month=11, day=2), datetime(year=2018, month=10, day=2), datetime(year=2015, month=11, day=3)]
    print(total_size(dates1))

    print("array of numpy datetime64 objects")
    dates2 = np.array(['2018-11-02', '2018-10-02', '2015-11-03'], dtype='datetime64')
    print(total_size(dates2))
