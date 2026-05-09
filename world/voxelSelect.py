from typing import TYPE_CHECKING
import glm

from engine.settings import (
    CHUNK_AREA,
    CHUNK_SIZE,
    MAX_RAY_DIST,
    WORLD_AREA,
    WORLD_D,
    WORLD_H,
    WORLD_W,
)


if TYPE_CHECKING:
    from world.world import World


class VoxelSelect:
    def __init__(self, world: World) -> None:
        self.world = world
        self.engine = world.engine
        # rayCast在更新
        self.selected_voxel_normal = glm.ivec3(0)
        self.selected_voxel_id = 0
        self.selected_voxel_world_pos = glm.ivec3(0)
        self.selected_voxel_local_pos = glm.ivec3(0)
        self.selected_chunk_index = 0
        self.selected_voxel_index = 0

    def rayCast(self):
        start_x, start_y, start_z = self.engine.player.position.xyz
        end_x, end_y, end_z = (
            self.engine.player.position + MAX_RAY_DIST * self.engine.player.forward
        )
        current_voxel_pos = glm.ivec3(self.engine.player.position)
        self.selected_voxel_normal = glm.ivec3(0)
        self.selected_voxel_id = 0
        hit_face = -1

        direct_x = glm.sign(end_x - start_x)
        direct_y = glm.sign(end_y - start_y)
        direct_z = glm.sign(end_z - start_z)

        INFINITY = 1000000.0
        if direct_x != 0:
            speed_x = min(direct_x / (end_x - start_x), INFINITY)
        else:
            speed_x = INFINITY
        if direct_y != 0:
            speed_y = min(direct_y / (end_y - start_y), INFINITY)
        else:
            speed_y = INFINITY
        if direct_z != 0:
            speed_z = min(direct_z / (end_z - start_z), INFINITY)
        else:
            speed_z = INFINITY

        if direct_x > 0:
            dist_x = speed_x * (1.0 - glm.fract(start_x))
        else:
            dist_x = speed_x * glm.fract(start_x)
        if direct_y > 0:
            dist_y = speed_y * (1.0 - glm.fract(start_y))
        else:
            dist_y = speed_y * glm.fract(start_y)
        if direct_z > 0:
            dist_z = speed_z * (1.0 - glm.fract(start_z))
        else:
            dist_z = speed_z * glm.fract(start_z)

        while dist_x <= 1.0 or dist_y <= 1.0 or dist_z <= 1.0:
            voxel_id, chunk_index, voxel_index, voxel_local_pos = self._getVoxelInfo(
                current_voxel_pos
            )
            if voxel_id:
                if hit_face == 0:
                    self.selected_voxel_normal.x = -int(direct_x)
                if hit_face == 1:
                    self.selected_voxel_normal.y = -int(direct_y)
                if hit_face == 2:
                    self.selected_voxel_normal.z = -int(direct_z)
                self.selected_voxel_world_pos = current_voxel_pos
                # print(self.selected_voxel_world_pos)
                self.selected_voxel_id = voxel_id
                # print(self.selected_voxel_id)
                self.selected_chunk_index = chunk_index
                self.selected_voxel_index = voxel_index
                self.selected_voxel_local_pos = voxel_local_pos
                return True
            if dist_x > dist_y:
                if dist_y < dist_z:
                    dist_y += speed_y
                    current_voxel_pos.y += int(direct_y)
                    hit_face = 1
                else:
                    dist_z += speed_z
                    current_voxel_pos.z += int(direct_z)
                    hit_face = 2
            else:
                if dist_x < dist_z:
                    dist_x += speed_x
                    current_voxel_pos.x += int(direct_x)
                    hit_face = 0
                else:
                    dist_z += speed_z
                    current_voxel_pos.z += int(direct_z)
                    hit_face = 2
        return False

    def _getVoxelInfo(self, voxel_world_pos):
        dx, dy, dz = dxyz = voxel_world_pos // CHUNK_SIZE
        if 0 <= dx < WORLD_W and 0 <= dy < WORLD_H and 0 <= dz < WORLD_D:
            lx, ly, lz = voxel_local_pos = voxel_world_pos - dxyz * CHUNK_SIZE
            chunk_index = dx + dz * WORLD_W + dy * WORLD_AREA
            voxel_index = lx + lz * CHUNK_SIZE + ly * CHUNK_AREA
            voxel_id = self.world.world_voxels_id[chunk_index, voxel_index]
            return voxel_id, chunk_index, voxel_index, voxel_local_pos
        else:
            return 0, 0, 0, 0

    def addVoxel(self):
        if self.selected_voxel_id:
            new_voxels_world_pos = (
                self.selected_voxel_world_pos + self.selected_voxel_normal
            )
            voxel_id, chunk_index, voxel_index, voxel_local_pos = self._getVoxelInfo(
                new_voxels_world_pos
            )
            if not voxel_id:
                self.world.world_voxels_id[chunk_index, voxel_index] = 3
                self.world.chunks[chunk_index].chunk_mesh.updateVoxelsId(voxel_index, 3)
                self.world.chunks[chunk_index].chunk_mesh.buildChunkMesh()
                if self.world.chunks[chunk_index].chunk_mesh.is_all_zero:
                    self.world.chunks[chunk_index].chunk_mesh.is_all_zero = False
                self._rebuild_around_chunk_meshes(new_voxels_world_pos, voxel_local_pos)
                print("add one")

    def removeVoxel(self):
        if self.selected_voxel_id:
            self.world.world_voxels_id[
                self.selected_chunk_index, self.selected_voxel_index
            ] = 0
            self.world.chunks[self.selected_chunk_index].chunk_mesh.updateVoxelsId(
                self.selected_voxel_index, 0
            )
            self.world.chunks[self.selected_chunk_index].chunk_mesh.buildChunkMesh()
            self._rebuild_around_chunk_meshes(
                self.selected_voxel_world_pos, self.selected_voxel_local_pos
            )
            print("remove one")

    def _getChunkIndex(self, wx, wy, wz):
        ix = wx // CHUNK_SIZE
        iy = wy // CHUNK_SIZE
        iz = wz // CHUNK_SIZE
        if 0 <= ix < WORLD_W and 0 <= iy < WORLD_H and 0 <= iz < WORLD_D:
            return ix + iz * WORLD_W + iy * WORLD_AREA
        return -1

    def _rebuild_around_chunk_mesh(self, wx, wy, wz):
        chunk_index = self._getChunkIndex(wx, wy, wz)
        if chunk_index != -1:
            self.world.chunks[chunk_index].chunk_mesh.buildChunkMesh()

    def _rebuild_around_chunk_meshes(self, voxel_world_pos, voxel_local_pos):
        wx, wy, wz = voxel_world_pos
        lx, ly, lz = voxel_local_pos
        if lx == 0:
            self._rebuild_around_chunk_mesh(wx - 1, wy, wz)
        if lx == CHUNK_SIZE - 1:
            self._rebuild_around_chunk_mesh(wx + 1, wy, wz)
        if ly == 0:
            self._rebuild_around_chunk_mesh(wx, wy - 1, wz)
        if ly == CHUNK_SIZE - 1:
            self._rebuild_around_chunk_mesh(wx, wy + 1, wz)
        if lz == 0:
            self._rebuild_around_chunk_mesh(wx, wy, wz - 1)
        if lz == CHUNK_SIZE - 1:
            self._rebuild_around_chunk_mesh(wx, wy, wz + 1)

    def update(self):
        self.rayCast()
