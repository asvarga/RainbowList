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
def dB(i): return dG(i) << 1

# hop targets
def R(i): return i-dR(i)
def G(i): return i-dG(i)
def B(i): return i-dB(i)

@dataclass
class Node(object): 
    v: Any              # value
    i: int              # index
    n: 'Node' = None    # next
    r: 'Node' = None    # red
    g: 'Node' = None    # green
    b: 'Node' = None    # blue
    def cons(self, v):              # prepend value v onto this list
        i = self.i+1
        n = self
        k = i & -i
        # red
        if k == 1:          r = None
        elif k == 2:        r = n
        else:               r = n.b
        # green
        if k == 1:          g = n
        else:               g = r.g
        # blue
        if i & (k<<1):
            if i & (k<<2):  b = g.b
            else:           b = g
        elif i > (k<<1):
            if k == 1:      b = n.n
            else:           b = r.b.g
        else:               b = None
        return Node(v, i, n, r, g, b)
    def __getitem__(self, i):       # seek to self.i-i and return value
        if isinstance(i, slice):
            i = i.start
            return self.seek(self.i-i if i >= 0 else -i)
        return self.seek(self.i-i if i >= 0 else -i).v
    def seek(self, i):              # find node indexed i
        if i == self.i: return self
        if G(self.i) >= i and G(G(self.i)) >= G(i): return self.g.seek(i)
        if B(self.i) >= i and G(B(self.i)) >= G(i): return self.b.seek(i)
        if R(self.i) >= i and G(R(self.i)) >= G(i): return (self.r or self.n).seek(i)
        return self.n.seek(i)
    def __len__(self): return self.i
    def __str__(self): return "N"+str(self.list())
    def list(self): return [self.v] + (self.n.list() if self.n else [])
    def debug(self):
        def i(n): return n.i if n else '_'
        return f"N({self.v}\ti={self.i}\tr={i(self.r)}\tg={i(self.g)}\tb={i(self.b)}\tn={i(self.n)})"

# non-oop interface
def cons(v, n): return n.cons(v) if n else Node(v, 1, n)
def get(n, i): return n and n[i]
def debug(n): return n and n.debug()
