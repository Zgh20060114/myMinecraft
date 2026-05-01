from typing import TYPE_CHECKING
from warnings import simplefilter
from glm import simplex, vec3
import glm
import numpy as np
from mesh import baseMesh
from mesh.baseMesh import BaseMesh
from engine.settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOL, WIN_SIZE

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine
    from world.world import World


class ChunkMesh(BaseMesh):
    def __init__(self, engine: VoxelEngine, world: World, position=glm.ivec3(0, 0, 0)):
        super().__init__(engine)
        self.sp = engine.shader_program_manage.chunk
        self.position = position
        self.vbo_format = "3u1 1u1 1u1"
        self.vbo_attribution = ("in_position", "in_voxel_id", "in_face_id")
        self.vbo_format_size = sum(int(form[0]) for form in self.vbo_format.split(" "))
        self.chunk_voxels_id = self.buildVoxelsId()
        self.world = world.world_voxels_id
        self.vao = self.getVAO()
        self.is_all_zero = False

    def getVertexBufferDate(self) -> np.ndarray:
        print(self.world[1, 1:10])
        return self.getChunkVBD(self.chunk_voxels_id, self.vbo_format_size)

    # 决定了当前voxel的有无和种类
    def buildVoxelsId(self):
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)
        bx, by, bz = self.position * CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + bx
                wz = z + bz
                wy = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                ly = min(wy - by, CHUNK_SIZE)
                for y in range(ly):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = by + y + 1

        if not np.any(voxels):
            self.is_all_zero = True
        return voxels

    def appendVD(self, vbd, index, *vds):
        for vd in vds:
            for v in vd:
                vbd[index] = v
                index += 1
        return index

    def getChunkVBD(self, chunk_voxels_id, vbo_format_size):
        vbd = np.zeros(
            CHUNK_VOL * 36 * vbo_format_size, dtype=np.uint8
        )  # TODO: 我认为应该是36
        vbd_index = 0
        # 其实xyz的顺序对遍历没有影响
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    voxel_id = chunk_voxels_id[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                    if not voxel_id:
                        continue
                    # cull_face 面剔除,要求三角形顶点逆时针传递,从立方体外面看,不能透过别的面来看,不然就不叫面剔除了
                    # 顶面
                    if (
                        y == CHUNK_SIZE - 1
                        or chunk_voxels_id[x + CHUNK_SIZE * z + CHUNK_AREA * (y + 1)]
                        == 0
                    ):
                        v0 = (x, y + 1, z, voxel_id, 0)
                        v1 = (x + 1, y + 1, z, voxel_id, 0)
                        v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                        v3 = (x, y + 1, z + 1, voxel_id, 0)
                        vbd_index = self.appendVD(
                            vbd, vbd_index, v0, v3, v2, v0, v2, v1
                        )
                    # 底面
                    if (
                        y == 0
                        or chunk_voxels_id[x + CHUNK_SIZE * z + CHUNK_AREA * (y - 1)]
                        == 0
                    ):
                        v0 = (x, y, z, voxel_id, 1)
                        v1 = (x + 1, y, z, voxel_id, 1)
                        v2 = (x + 1, y, z + 1, voxel_id, 1)
                        v3 = (x, y, z + 1, voxel_id, 1)
                        vbd_index = self.appendVD(
                            vbd, vbd_index, v0, v2, v3, v0, v1, v2
                        )
                    # 右面
                    if (
                        x == CHUNK_SIZE - 1
                        or chunk_voxels_id[x + 1 + CHUNK_SIZE * z + CHUNK_AREA * y] == 0
                    ):
                        v0 = (x + 1, y, z, voxel_id, 2)
                        v1 = (x + 1, y, z + 1, voxel_id, 2)
                        v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                        v3 = (x + 1, y + 1, z, voxel_id, 2)
                        vbd_index = self.appendVD(
                            vbd, vbd_index, v0, v3, v2, v0, v2, v1
                        )
                    # 左面
                    if (
                        x == 0
                        or chunk_voxels_id[x - 1 + CHUNK_SIZE * z + CHUNK_AREA * y] == 0
                    ):
                        v0 = (x, y, z, voxel_id, 3)
                        v1 = (x, y, z + 1, voxel_id, 3)
                        v2 = (x, y + 1, z + 1, voxel_id, 3)
                        v3 = (x, y + 1, z, voxel_id, 3)
                        vbd_index = self.appendVD(
                            vbd, vbd_index, v0, v2, v3, v0, v1, v2
                        )
                    # 前面
                    if (
                        z == CHUNK_SIZE - 1
                        or chunk_voxels_id[x + CHUNK_SIZE * (z + 1) + CHUNK_AREA * y]
                        == 0
                    ):
                        v0 = (x, y, z + 1, voxel_id, 4)
                        v1 = (x, y + 1, z + 1, voxel_id, 4)
                        v2 = (x + 1, y + 1, z + 1, voxel_id, 4)
                        v3 = (x + 1, y, z + 1, voxel_id, 4)
                        vbd_index = self.appendVD(
                            vbd, vbd_index, v0, v3, v2, v0, v2, v1
                        )
                    # 后面
                    if (
                        z == 0
                        or chunk_voxels_id[x + CHUNK_SIZE * (z - 1) + CHUNK_AREA * y]
                        == 0
                    ):
                        v0 = (x, y, z, voxel_id, 5)
                        v1 = (x, y + 1, z, voxel_id, 5)
                        v2 = (x + 1, y + 1, z, voxel_id, 5)
                        v3 = (x + 1, y, z, voxel_id, 5)
                        vbd_index = self.appendVD(
                            vbd, vbd_index, v0, v2, v3, v0, v1, v2
                        )
        return vbd[: vbd_index + 1]
