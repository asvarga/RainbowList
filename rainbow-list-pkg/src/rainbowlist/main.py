#!/usr/local/bin/python3.7

# an implementatino of Rainbow Lists: pure lists with O(log(i)) indexing and O(1) cons
# this implementation attempts to use bit operations in place of pointer lookups whenever possible
# https://github.com/asvarga

####

from dataclasses import dataclass
from typing import Any

####

# hop deltas
def dR(i): return dG(i) >> 1
def dG(i): return i & -i
def dY(i): return dR(i+dG(i))
def dN(i): return 1

# hop targets
def R(i): return i-dR(i)
def G(i): return i-dG(i)
def Y(i): return R(i+dG(i))
def N(i): return i-dN(i)

@dataclass
class Node(object):
    v: Any              # value
    i: int              # index
    n: 'Node' = None    # next
    r: 'Node' = None    # red
    g: 'Node' = None    # green
    y: 'Node' = None    # yellow
    def cons(self, v):              # prepend value v onto this list
        i = self.i+1
        n = self
        if i % 2:
            r = None
            g = n
        else:
            r = n.y or n
            g = r.g
        y = Y(i) != i and (g.y or g)
        return Node(v, i, n, r, g, y)
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
def cons(v, n): return n.cons(v) if n else Node(v, 1, n)
def get(n, i): return n and n[i]
def val(n): return n and n.v
def debug(n): return n and n.debug()
