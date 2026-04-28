from typing import TYPE_CHECKING
import numpy as np
from mesh.baseMesh import BaseMesh
from engine.settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOL

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class ChunkMesh(BaseMesh):
    def __init__(self, engine: VoxelEngine):
        super().__init__(engine)
        self.sp = engine.shader_program_manage.chunk
        self.vbo_format = "3u1 1u1 1u1"
        self.vbo_attribution = ("in_position", "voxel_id", "face_id")
        self.vbo_format_size = sum(int(form[0]) for form in self.vbo_format.split(" "))
        self.vao = self.getVAO()
        self.chunk_voxels_id = self.buildVoxelsId()

    def getVertexBufferDate(self) -> np.ndarray:
        self.getChunkVBD(self.chunk_voxels_id, self.vbo_format)

    def buildVoxelsId(self):
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)

        for z in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[z * CHUNK_AREA + x * CHUNK_SIZE + y] = 1
        return voxels

    def getChunkVBD(self, chunk_voxels_id, vbo_format_size):
        vbd = np.zeros(
            CHUNK_VOL * 36 * vbo_format_size, dtype=np.uint8
        )  # TODO: 我认为应该是36
        vbd_index = 0
        # 其实xyz的顺序对遍历没有影响
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for x in range(CHUNK_SIZE):
                    voxel_id = self.chunk_voxels_id[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                    if not voxel_id:
                        continue
                    # 顶面
