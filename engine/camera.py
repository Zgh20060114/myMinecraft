import glm


class Camera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 3.0), pitch=0, yaw=-90) -> None:
        self.position = glm.vec3(position)
        self.pitch = glm.radians(pitch)
        self.yaw = glm.radians(yaw)

        self.world_up = glm.vec3(0.0,1.0,0.0)

        self.up = self.world_up
        self.foward = glm.vec3(0.0,0.0,-1.0)
        self.right = glm.vec3(1.0,0.0,0.0)
    def update_camera():

