import numpy as np
import moderngl as mgl
from engine.settings import ASPECT_RATIO

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class CrosshairMesh:
    def __init__(self, engine: VoxelEngine):
        self.ctx = engine.context
        size = 0.03
        aspect = ASPECT_RATIO

        vertex_data = np.array(
            [
                -size / aspect,
                0.0,
                0.0,
                size / aspect,
                0.0,
                0.0,
                0.0,
                -size,
                0.0,
                0.0,
                size,
                0.0,
            ],
            dtype="f4",
        )

        self.vbo = self.ctx.buffer(vertex_data)
        self.program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec3 in_position;
                void main() {
                    gl_Position = vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                out vec4 fragColor;
                void main() {
                    fragColor = vec4(1.0, 1.0, 1.0, 1.0);
                }
            """,
        )
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, "in_position")

    def render(self):
        # 绘制准星时禁用深度测试，确保它永远在最前面
        self.ctx.disable(mgl.DEPTH_TEST)
        self.vao.render(mgl.LINES)
        self.ctx.enable(mgl.DEPTH_TEST)
