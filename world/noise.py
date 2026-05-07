from functools import cache
from opensimplex.internals import _noise2, _init
from numba import njit

perm, _ = _init(12)


@njit(cache=True)
def _noise(wx, wz):
    return int(_noise2(wx * 0.03, wz * 0.03, perm) * 32 + 32)
