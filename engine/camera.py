import glm

from engine.settings import ASPECT_RATIO, FAR, NEAR, PITCH_MAX, V_FOV


class Camera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 3.0), pitch=0, yaw=-90) -> None:
        self.position = glm.vec3(position)
        self.pitch = glm.radians(pitch)
        self.yaw = glm.radians(yaw)

        self.world_up = glm.vec3(0.0, 1.0, 0.0)

        self.up = self.world_up
        self.forward = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)

        self.view_matrix = glm.mat4()
        self.projection_matrix = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.model_matrix = glm.mat4(1.0)

    def updateCameraVector(self):
        # yaw是从-90开始的
        forward = glm.vec3()
        forward.x = glm.cos(self.pitch) * glm.cos(self.yaw)
        forward.y = glm.sin(self.pitch)
        forward.z = glm.cos(self.pitch) * glm.sin(self.yaw)

        self.forward = glm.normalize(forward)
        self.right = glm.normalize(glm.cross(self.forward, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def updateViewMatrix(self):
        self.view_matrix = glm.lookAt(
            self.position, self.position + self.forward, self.up
        )

    def update(self):
        self.updateCameraVector()
        self.updateViewMatrix()

    def rotatePitch(self, delta_pitch):
        self.pitch += delta_pitch
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotateYaw(self, delt_yaw):
        self.yaw -= delt_yaw

    def move_forward(self, velocity):
        self.position += self.forward * velocity

    def move_backward(self, velocity):
        self.position -= self.forward * velocity

    def move_right(self, velocity):
        self.position += self.right * velocity

    def move_left(self, velocity):
        self.position -= self.right * velocity

    def move_up(self, velocity):
        self.position += self.up * velocity

    def move_down(self, velocity):
        self.position -= self.up * velocity
