

from rainbowlist import *
from math import floor, sqrt

def test0():
    N = 10
    node = None

    for i in range(1, N+1):
        node = cons(i*i, node)
        assert node.i == i

    for i in range(0, N):
        assert node[i] == (N-i)**2

    for i in range(1, N*N+1):
        assert floor(sqrt(node.find(lambda v: v <= i).v)) == floor(sqrt(i))

def test1():
    N = 10
    assert N % 2 == 0   # tests below assume this
    node = None
    keep = []       # keep track of nodes to prevent garbage collection

    for i in range(1, N+1):
        node = wcons(i*i, node)
        keep.append(node)
        assert node.i == i

    for i in range(0, N):
        assert node[i] == (N-i)**2

    for i in range(1, N*N+1):
        assert floor(sqrt(node.find(lambda v: v <= i).v)) == floor(sqrt(i))

    assert node[N//2] is not None

    keep = keep[N//2:]  # dump half the nodes

    for i in range(N//2):
        assert node[i] == (N-i)**2

    for i in range((N//2+1)**2, N*N+1):
        assert floor(sqrt(node.find(lambda v: v <= i).v)) == floor(sqrt(i))

    assert node[N//2] is None


if __name__ == "__main__":
    test0()
    print("test0: OK")
    test1()
    print("test1: OK")
