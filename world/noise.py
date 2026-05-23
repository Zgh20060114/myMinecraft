from opensimplex.internals import _noise2, _init
from numba import njit

perm, _ = _init(12)


@njit(cache=True)  # 编译成机器码,并缓存到硬盘
def noise2(wx, wz):
    return _noise2(wx, wz, perm)
