from engine.settings import CHUNK_VOL, WORLD_AREA, WORLD_D, WORLD_H, WORLD_VOL, WORLD_W
import numpy as np

from typing import TYPE_CHECKING

from world.chunk import Chunk
import glm

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class World:
    def __init__(self, engine: "VoxelEngine") -> None:
        self.engine = engine
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels_id = np.zeros([WORLD_VOL, CHUNK_VOL], dtype="uint8")
        self.buidChunksVoxelsID()

    def buidChunksVoxelsID(self):
        for x in range(WORLD_W):
            for z in range(WORLD_D):
                for y in range(WORLD_H):
                    chunks_index = x + z * WORLD_W + y * WORLD_AREA
                    self.chunks[chunks_index] = Chunk(
                        self.engine, position=glm.vec3(x, y, z)
                    )
                    self.voxels_id[chunks_index] = self.chunks[
                        chunks_index
                    ].chunkMesh.chunk_voxels_id

    def render(self):
        for chunk in self.chunks:
            chunk.render()
