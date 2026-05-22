from typing import TYPE_CHECKING
import math
import glm
from engine.settings import CHUNK_SPHERE_RADIUS, FAR, H_FOV, NEAR, V_FOV

if TYPE_CHECKING:
    from engine.camera import Camera
    from world.chunk import Chunk


class Frustum:
    def __init__(self, camera: Camera):
        self.camera = camera
        self.scale_h = 1.0 / math.cos(half_h := H_FOV / 2)
        self.tan_h = math.tan(half_h)
        self.scale_v = 1.0 / math.cos(half_v := V_FOV / 2)
        self.tan_v = math.tan(half_v)

    def isOnFrustum(self, chunk: Chunk):
        vector_sphere_and_camera = glm.vec3(chunk.chunk_center) - self.camera.position
        dist_z = glm.dot(vector_sphere_and_camera, self.camera.forward)
        if not ((NEAR - CHUNK_SPHERE_RADIUS) <= dist_z <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        dist_x = glm.dot(vector_sphere_and_camera, self.camera.right)
        dist_max_x = dist_z * self.tan_h + CHUNK_SPHERE_RADIUS * self.scale_h
        if not (-dist_max_x <= dist_x <= dist_max_x):
            return False
        dist_y = glm.dot(vector_sphere_and_camera, self.camera.up)
        dist_max_y = dist_z * self.tan_v + CHUNK_SPHERE_RADIUS * self.scale_v
        if not (-dist_max_y <= dist_y <= dist_max_y):
            return False

        return True
