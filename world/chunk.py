from typing import TYPE_CHECKING
import numpy as np
from engine.settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOL
from mesh.chunkMesh import ChunkMesh

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Chunk:
    def __init__(self, engine: VoxelEngine):
        self.engine = engine
        self.voxels = self.buildVoxels()
        self.chunkMesh = ChunkMesh(self)

    def buildVoxels(self):
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)

        for z in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[z * CHUNK_AREA + x * CHUNK_SIZE + y] = 1
        return voxels

    def render(self):
        self.chunkMesh.render()
