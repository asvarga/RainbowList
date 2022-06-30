

from rainbowlist import *
from math import floor, sqrt

def test0():
    N = 10
    node = None

    for i in range(1, N+1):
        node = cons(i*i, node)
        assert node.i == i

    for i in range(0, N):
        node[i] == N-i

    for i in range(1, N*N+1):
        assert floor(sqrt(node.find(lambda v: v <= i).v)) == floor(sqrt(i))


if __name__ == "__main__":
    test0()
    print("test0: OK")
