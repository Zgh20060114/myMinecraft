from typing import TYPE_CHECKING
import glm
import numba
import numpy as np
from world.noise import _noise
from mesh.baseMesh import BaseMesh
from engine.settings import (
    CHUNK_AREA,
    CHUNK_SIZE,
    CHUNK_VOL,
    WIN_SIZE,
    WORLD_AREA,
    WORLD_D,
    WORLD_H,
    WORLD_W,
)

if TYPE_CHECKING:
    from world.world import World

FLIP_MODE = False


class ChunkMesh(BaseMesh):
    def __init__(self, world: World, position=glm.ivec3(0, 0, 0)):
        super().__init__(world.engine)
        self.sp = world.engine.shader_program_manage.chunk
        self.position = position
        self.vbo_format = "3u1 1u1 1u1 1u1 1u1"
        self.vbo_attribution = (
            "in_position",
            "in_voxel_id",
            "in_face_id",
            "in_ao_id",
            "in_flip_id",
        )
        self.vbo_format_size = sum(int(form[0]) for form in self.vbo_format.split(" "))
        self.chunk_voxels_id = self.buildVoxelsId()
        self.vao = None
        self.is_all_zero = False
        self.world_voxels_id = world.world_voxels_id

    def buildChunkMesh(self):
        self.vao = self.getVAO()

    def updateVoxelsId(self, voxel_index, id):
        self.chunk_voxels_id[voxel_index] = id

    def getVertexBufferDate(self) -> np.ndarray:
        return self.getChunkVBD(self.chunk_voxels_id, self.vbo_format_size)

    # 决定了当前voxel的有无和种类
    def buildVoxelsId(self):
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)
        bx, by, bz = self.position * CHUNK_SIZE
        self._generateTerrain(bx, by, bz, voxels)
        if not np.any(voxels):
            self.is_all_zero = True
        return voxels

    @staticmethod
    @numba.njit
    def _generateTerrain(bx, by, bz, voxels):
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + bx
                wz = z + bz
                wy = _noise(wx, wz)
                ly = min(wy - by, CHUNK_SIZE)
                for y in range(ly):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (by + y + 1) % 7 + 1

    def appendVD(self, vbd, index, *vds):
        for vd in vds:
            for v in vd:
                vbd[index] = v
                index += 1
        return index

    def getChunkIndex(self, wx, wy, wz):
        ix = wx // CHUNK_SIZE
        iy = wy // CHUNK_SIZE
        iz = wz // CHUNK_SIZE
        if 0 <= ix < WORLD_W and 0 <= iy < WORLD_H and 0 <= iz < WORLD_D:
            return ix + iz * WORLD_W + iy * WORLD_AREA
        return -1

    def isEmpty(self, wx, wy, wz):
        chunk_index = self.getChunkIndex(wx, wy, wz)
        if chunk_index == -1:
            return True
        chunk_voxels_id = self.world_voxels_id[chunk_index]
        lx = wx % CHUNK_SIZE
        ly = wy % CHUNK_SIZE
        lz = wz % CHUNK_SIZE
        if chunk_voxels_id[lx + CHUNK_SIZE * lz + CHUNK_AREA * ly] == 0:
            return True
        return False

    def getAmbientOcclusion(self, wx, wy, wz, plane):
        if plane == "Y":
            a = self.isEmpty(wx, wy, wz - 1)
            b = self.isEmpty(wx - 1, wy, wz - 1)
            c = self.isEmpty(wx - 1, wy, wz)
            d = self.isEmpty(wx - 1, wy, wz + 1)
            e = self.isEmpty(wx, wy, wz + 1)
            f = self.isEmpty(wx + 1, wy, wz + 1)
            g = self.isEmpty(wx + 1, wy, wz)
            h = self.isEmpty(wx + 1, wy, wz - 1)
        if plane == "X":
            a = self.isEmpty(wx, wy, wz - 1)
            b = self.isEmpty(wx, wy - 1, wz - 1)
            c = self.isEmpty(wx, wy - 1, wz)
            d = self.isEmpty(wx, wy - 1, wz + 1)
            e = self.isEmpty(wx, wy, wz + 1)
            f = self.isEmpty(wx, wy + 1, wz + 1)
            g = self.isEmpty(wx, wy + 1, wz)
            h = self.isEmpty(wx, wy + 1, wz - 1)
        if plane == "Z":
            a = self.isEmpty(wx - 1, wy, wz)
            b = self.isEmpty(wx - 1, wy - 1, wz)
            c = self.isEmpty(wx, wy - 1, wz)
            d = self.isEmpty(wx + 1, wy - 1, wz)
            e = self.isEmpty(wx + 1, wy, wz)
            f = self.isEmpty(wx + 1, wy + 1, wz)
            g = self.isEmpty(wx, wy + 1, wz)
            h = self.isEmpty(wx - 1, wy + 1, wz)
        return (
            a + b + c,
            c + d + e,
            e + f + g,
            g + h + a,
        )  ## 上左前和下右后应该分开,都遵循逆时针,这里每分开,直接在赋值的时候改了

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

                    bx, by, bz = self.position * CHUNK_SIZE
                    wx = x + bx
                    wz = z + bz
                    wy = y + by

                    # cull_face 面剔除,要求三角形顶点逆时针传递,从立方体外面看,不能透过别的面来看,不然就不叫面剔除了
                    # 顶面
                    if self.isEmpty(wx, wy + 1, wz):
                        ao = self.getAmbientOcclusion(wx, wy + 1, wz, plane="Y")
                        flip_id = ao[1] + ao[3] < ao[0] + ao[2]
                        v0 = (x, y + 1, z + 1, voxel_id, 2, ao[1], flip_id)
                        v1 = (x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                        v2 = (x + 1, y + 1, z, voxel_id, 2, ao[3], flip_id)
                        v3 = (x, y + 1, z, voxel_id, 2, ao[0], flip_id)
                        if FLIP_MODE:
                            vbd_index = self.appendVD(
                                vbd, vbd_index, v0, v2, v3, v0, v1, v2
                            )
                        else:
                            if not flip_id:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v0, v2, v3, v0, v1, v2
                                )
                            else:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v1, v2, v3, v1, v3, v0
                                )
                    # 底面
                    if self.isEmpty(wx, wy - 1, wz):
                        ao = self.getAmbientOcclusion(wx, wy - 1, wz, plane="Y")
                        flip_id = ao[0] + ao[2] < ao[1] + ao[3]
                        v0 = (x, y, z, voxel_id, 0, ao[0], flip_id)
                        v1 = (x + 1, y, z, voxel_id, 0, ao[3], flip_id)
                        v2 = (x + 1, y, z + 1, voxel_id, 0, ao[2], flip_id)
                        v3 = (x, y, z + 1, voxel_id, 0, ao[1], flip_id)
                        if FLIP_MODE:
                            vbd_index = self.appendVD(
                                vbd, vbd_index, v0, v2, v3, v0, v1, v2
                            )
                        else:
                            if not flip_id:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v0, v2, v3, v0, v1, v2
                                )
                            else:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v1, v2, v3, v1, v3, v0
                                )
                    # 左面
                    if self.isEmpty(wx - 1, wy, wz):
                        ao = self.getAmbientOcclusion(wx - 1, wy, wz, plane="X")
                        flip_id = ao[0] + ao[2] < ao[1] + ao[3]
                        v0 = (x, y, z, voxel_id, 1, ao[0], flip_id)
                        v1 = (x, y, z + 1, voxel_id, 1, ao[1], flip_id)
                        v2 = (x, y + 1, z + 1, voxel_id, 1, ao[2], flip_id)
                        v3 = (x, y + 1, z, voxel_id, 1, ao[3], flip_id)
                        if FLIP_MODE:
                            vbd_index = self.appendVD(
                                vbd, vbd_index, v0, v2, v3, v0, v1, v2
                            )
                        else:
                            if not flip_id:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v0, v2, v3, v0, v1, v2
                                )
                            else:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v1, v2, v3, v1, v3, v0
                                )
                    # 右面
                    if self.isEmpty(wx + 1, wy, wz):
                        ao = self.getAmbientOcclusion(wx + 1, wy, wz, plane="X")
                        flip_id = ao[1] + ao[3] < ao[0] + ao[2]
                        v0 = (x + 1, y, z + 1, voxel_id, 3, ao[1], flip_id)
                        v1 = (x + 1, y, z, voxel_id, 3, ao[0], flip_id)
                        v2 = (x + 1, y + 1, z, voxel_id, 3, ao[3], flip_id)
                        v3 = (x + 1, y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                        if FLIP_MODE:
                            vbd_index = self.appendVD(
                                vbd, vbd_index, v0, v2, v3, v0, v1, v2
                            )
                        else:
                            if not flip_id:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v0, v2, v3, v0, v1, v2
                                )
                            else:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v1, v2, v3, v1, v3, v0
                                )
                    # 前面
                    # 全错了,应该固定v0的位置
                    if self.isEmpty(wx, wy, wz + 1):
                        ao = self.getAmbientOcclusion(wx, wy, wz + 1, plane="Z")
                        flip_id = ao[0] + ao[2] < ao[1] + ao[3]
                        v0 = (x, y, z + 1, voxel_id, 4, ao[0], flip_id)
                        v1 = (x + 1, y, z + 1, voxel_id, 4, ao[1], flip_id)
                        v2 = (x + 1, y + 1, z + 1, voxel_id, 4, ao[2], flip_id)
                        v3 = (x, y + 1, z + 1, voxel_id, 4, ao[3], flip_id)
                        if FLIP_MODE:
                            vbd_index = self.appendVD(
                                vbd, vbd_index, v0, v2, v3, v0, v1, v2
                            )
                        else:
                            if not flip_id:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v0, v2, v3, v0, v1, v2
                                )
                            else:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v1, v2, v3, v1, v3, v0
                                )
                    # 后面
                    if self.isEmpty(wx, wy, wz - 1):
                        ao = self.getAmbientOcclusion(wx, wy, wz - 1, plane="Z")
                        flip_id = ao[1] + ao[3] < ao[0] + ao[2]
                        v0 = (x + 1, y, z, voxel_id, 5, ao[1], flip_id)
                        v1 = (x, y, z, voxel_id, 5, ao[0], flip_id)
                        v2 = (x, y + 1, z, voxel_id, 5, ao[3], flip_id)
                        v3 = (x + 1, y + 1, z, voxel_id, 5, ao[0], flip_id)
                        if FLIP_MODE:
                            vbd_index = self.appendVD(
                                vbd, vbd_index, v0, v2, v3, v0, v1, v2
                            )
                        else:
                            if not flip_id:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v0, v2, v3, v0, v1, v2
                                )
                            else:
                                vbd_index = self.appendVD(
                                    vbd, vbd_index, v1, v2, v3, v1, v3, v0
                                )
        return vbd[: vbd_index + 1]
