from engine.settings import CHUNK_VOL, WORLD_AREA, WORLD_D, WORLD_H, WORLD_VOL, WORLD_W
import numpy as np

from typing import TYPE_CHECKING

from world.chunk import Chunk
from world.voxelSelect import VoxelSelect
import glm

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class World:
    def __init__(self, engine: "VoxelEngine") -> None:
        self.engine = engine
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.world_voxels_id = np.zeros([WORLD_VOL, CHUNK_VOL], dtype="uint8")
        self._buidChunksVoxelsID()
        self._buildWorldMeshes()
        self.voxel_select = VoxelSelect(self)

    def _buidChunksVoxelsID(self):
        for x in range(WORLD_W):
            for z in range(WORLD_D):
                for y in range(WORLD_H):
                    chunks_index = x + z * WORLD_W + y * WORLD_AREA
                    self.chunks[chunks_index] = Chunk(self, position=glm.ivec3(x, y, z))
                    self.world_voxels_id[chunks_index] = self.chunks[
                        chunks_index
                    ].chunk_mesh.chunk_voxels_id  # 得益于python的赋值都是传递地址(引用),所以访问的是一个东西

    def _buildWorldMeshes(self):
        for chunk in self.chunks:
            chunk.chunk_mesh.buildChunkMesh()

    def render(self):
        for chunk in self.chunks:
            chunk.render()

    def update(self):
        self.voxel_select.update()
