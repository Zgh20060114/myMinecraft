from moderngl import NEAREST
import numba as njit
import glm

height = 1080
width = 1920
WIN_SIZE = (width, height)

BG_COLOR = (1.0, 0.5, 0.5)

# 摄像机画面宽高比
ASPECT_RATIO = WIN_SIZE[0] / WIN_SIZE[1]
V_FOV = glm.radians(50)
H_FOV = glm.atan(glm.tan(V_FOV / 2) * ASPECT_RATIO)
NEAR = 0.1
FAR = 2000
PITCH_MAX = glm.radians(89)
