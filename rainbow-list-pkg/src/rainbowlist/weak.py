#!/usr/local/bin/python3.7

# an implementatino of Rainbow Lists: pure lists with O(log(i)) indexing and O(1) cons
# this implementation attempts to use bit operations in place of pointer lookups whenever possible
# https://github.com/asvarga

# this is a version with all weak references between nodes
# you'll need to hold strong references to all nodes you want to keep

####

from dataclasses import dataclass
from .main import *
from typing import Any
import weakref

####

def nref(): return None
def ref(n): return weakref.ref(n) if n else nref
# def ref(n): return n if isinstance(n, weakref.ref) else weakref.ref(n) if n else nref


@dataclass
class WeakNode:
    v: Any              # value
    i: int              # index
    _n: Any = None       # next
    _r: Any = None      # red
    _g: Any = None      # green
    _y: Any = None      # yellow

    # note: references may be None, a weakref to None, or a weakref to a Node
    @property
    def n(self): return self._n and self._n()
    @property
    def r(self): return self._r and self._r()
    @property
    def g(self): return self._g and self._g()
    @property
    def y(self): return self._y and self._y()

    def cons(self, v):              # prepend value v onto this list
        i = self.i+1
        _n = ref(self)
        if i % 2:
            _r = None
            _g = _n
        else:
            _r = self._y or _n
            _g = _r()._g if _r() else nref
        _y = Y(i) != i and ((_g()._y if _g() else nref) or _g)
        return WeakNode(v, i, _n, _r, _g, _y)

    def __getitem__(self, i):       # seek to self.i-i and return value
        isSlice = isinstance(i, slice)
        i = i.start if isSlice else i
        if not 0 <= i <= self.i:
            raise IndexError(f'index {i} out of range')
        n = self.seek(self.i-i if i >= 0 else -i)
        return n if isSlice else val(n)
    def seek(self, i):
        n = self
        while n and n.i != i:
            n = n.y if n.i > Y(n.i) >= i else n.g if G(n.i) >= i else n.r if R(n.i) >= i else n.n
        return n
    def find(self, pred):
        n = self
        while n and not pred(n.v):
            n = next(filter(lambda n: n and not pred(n.v), [n.y, n.g, n.r]), n.n)
        return n
    def __len__(self): return self.i
    def __str__(self): return "N"+str(list(self))
    def __iter__(self):
        n = self
        while n:
            yield n.v
            n = n.n
    def debug(self):
        def i(n): return n.i if n else '_'
        return f"N({self.v}\ti={self.i}\tr={i(self.r)}\tg={i(self.g)}\ty={i(self.y)}\tn={i(self.n)})"

# non-oop interface
def wcons(v, n): return n.cons(v) if n else WeakNode(v, 1, n)
