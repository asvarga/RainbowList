# RainbowList

An implementation of Rainbow Lists, which are pure lists with O(log(i)) indexing and constant-time cons.

See [this blog post](https://medium.com/p/a607d06234e0).

![A Rainbow List of length n=63 indexed by i=60](pics/arcs_63_3.png)

### Files
- [rainbowList.py](./rainbowList.py): Original implementation.
- [rainbowList_noY.py](./rainbowList_noY.py): Optimized to use only 3 shortcuts per node.
- [rainbowList.ipynb](./rainbowList.ipynb): Jupyter notebook for experiments/diagrams.
- [rainbow_list/src/main.rs](./rainbow_list/src/main.rs): Rust implementation (of noY)
    - Based heavily on: https://rust-unofficial.github.io/too-many-lists

### TODO

- implement indexing
- improve code like `n.as_ref().and_then(|x| x.b.clone())`
    - use a macro or implementation?