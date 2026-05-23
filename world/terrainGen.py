import math
from os import scandir
from random import random

from engine.settings import (
    CENTER_XZ,
    CENTER_Y,
    CHUNK_AREA,
    CHUNK_SIZE,
    DIRT,
    DIRT_LVL,
    GRASS,
    GRASS_LVL,
    H_TREE_HEIGHT,
    H_TREE_WIDTH,
    LEAVES,
    SAND,
    SAND_LVL,
    SNOW,
    SNOW_LVL,
    STONE,
    STONE_LVL,
    TREE_HEIGHT,
    TREE_PROBABILITY,
    WOOD,
)
from world.noise import noise2, noise3
from numba import njit


@njit
def getHeight(wx, wz):
    amp1 = CENTER_Y
    amp2 = 0.5 * amp1
    amp3 = 0.5 * amp2
    amp4 = 0.5 * amp3

    if noise2(wx * 0.05, wz * 0.05) < 0:
        amp1 /= 1.07

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


@njit
def getIndex(
    x,
    y,
    z,
):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def setVoxelId(voxels, x, y, z, wx, wy, wz, world_height):
    if wy < (world_height - 1):
        if (
            noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0
            and noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10
        ):
            voxel_id = 0
        else:
            voxel_id = STONE
    else:
        ry = wy - int(7 * random())
        if ry > SNOW_LVL:
            voxel_id = SNOW
        elif ry > STONE_LVL:
            voxel_id = STONE
        elif ry > DIRT_LVL:
            voxel_id = DIRT
        elif ry > GRASS_LVL:
            voxel_id = GRASS
        else:
            voxel_id = SAND

        if GRASS_LVL < ry < DIRT_LVL:
            plantTree(voxels, x, y, z)

    voxels[getIndex(x, y, z)] = voxel_id


@njit
def plantTree(voxels, x, y, z):
    rand = random()
    if rand > TREE_PROBABILITY:
        return
    if x < H_TREE_WIDTH or x + H_TREE_WIDTH > CHUNK_SIZE - 1:
        return
    if z < H_TREE_WIDTH or z + H_TREE_WIDTH > CHUNK_SIZE - 1:
        return
    if y + TREE_HEIGHT > CHUNK_SIZE - 1:
        return
    for iy in range(1, H_TREE_HEIGHT + 1):
        voxels[getIndex(x, y + iy, z)] = WOOD
    rand01 = int(random() * 2)
    for iy in range(H_TREE_HEIGHT + 1, TREE_HEIGHT):
        for ix in range(-H_TREE_WIDTH + rand01, H_TREE_WIDTH - rand01):
            for iz in range(-H_TREE_WIDTH + rand01, H_TREE_WIDTH - rand01):
                if (ix + iz) % 4:
                    voxels[getIndex(x + ix, y + iy, z + iz)] = LEAVES
