import math

from engine.settings import CENTER_XZ, CENTER_Y
from world.noise import noise2
from numba import njit


@njit
def getHeight(wx, wz):
    amp1 = CENTER_Y
    amp2 = 0.5 * amp1
    amp3 = 0.5 * amp2
    amp4 = 0.5 * amp3

    if noise2(wx * 0.1, wz * 0.1) < 0:
        amp1 /= 1.1

    fre1 = 0.005
    fre2 = 2 * fre1
    fre3 = 2 * fre2
    fre4 = 2 * fre3

    height = 0
    height += noise2(wx * fre1, wz * fre1) * amp1 + amp1
    height += noise2(wx * fre2, wz * fre2) * amp2 - amp2
    height += noise2(wx * fre3, wz * fre3) * amp3 + amp3
    height += noise2(wx * fre4, wz * fre4) * amp4 - amp4

    height = max(noise2(wx * fre4, wz * fre4) + 2, height)

    island_mask = 1.0 / (
        pow(0.0025 * math.hypot(wx - CENTER_XZ, wz - CENTER_XZ), 20) + 0.0001
    )
    island_mask = min(island_mask, 1.0)
    return int(height * island_mask)
