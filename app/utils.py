import numpy

def ismember(a, b):
    bind = {}
    for elt in b:
        if elt not in bind:
            bind[elt] = True
    return numpy.array([bind.get(itm, False) for itm in a])
