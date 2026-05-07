from sys import set_int_max_str_digits
from typing import TYPE_CHECKING
import glm
from numba.core.bytecode import dis

from engine.settings import MAX_RAY_DIST


if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class VoxelHandler:
    def __init__(self, engine: VoxelEngine) -> None:
        self.engine = engine
        self.voxel_normal = glm.vec3(0)
        self.handled_voxel_world_pos = glm.vec3(0)

    def rayCast(self):
        start_x, start_y, start_z = self.engine.player.position.xyz
        end_x, end_y, end_z = (
            self.engine.player.position + MAX_RAY_DIST * self.engine.player.forward
        )
        current_voxel_pos = glm.ivec3(self.engine.player.position)
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
            speed_y = min(direct_x / (end_x - start_x), INFINITY)
        else:
            speed_y = INFINITY
        if direct_z != 0:
            speed_z = min(direct_x / (end_x - start_x), INFINITY)
        else:
            speed_z = INFINITY

        if direct_x > 0:
            dist_x = speed_x * (1.0 - glm.fract(start_x))
        else:
            dist_x = speed_x * glm.fract(start_x)
        if direct_y > 0:
            dist_y = speed_x * (1.0 - glm.fract(start_x))
        else:
            dist_y = speed_x * glm.fract(start_x)
        if direct_z > 0:
            dist_z = speed_x * (1.0 - glm.fract(start_x))
        else:
            dist_z = speed_x * glm.fract(start_x)

        while dist_x <= 1.0 and dist_y <= 1.0 and dist_z <= 1.0:
            result = self._getVoxelInfo(current_voxel_pos)
            if result:
                if hit_face == 0:
                    self.voxel_normal.x = -direct_x
                if hit_face == 1:
                    self.voxel_normal.y = -direct_y
                if hit_face == 2:
                    self.voxel_normal.z = -direct_z
                self.handled_voxel_world_pos = current_voxel_pos
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
                dist_x += speed_x
                current_voxel_pos.x += int(direct_x)
                hit_face = 0
