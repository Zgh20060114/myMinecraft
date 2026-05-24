from typing import TYPE_CHECKING
import numpy as np
from mesh.baseMesh import BaseMesh

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class WaterMesh(BaseMesh):
    def __init__(self, engine: VoxelEngine):
        super().__init__(engine)
        self.sp = engine.shader_program_manage.water
        self.vbo_format = "3u1 2u1"
        self.vbo_attribution = ("in_vertex_position", "in_texture_coord")
        self.vao = self.getVAO()

    def getVertexBufferDate(self) -> np.ndarray:
        # 面剔除顶点逆时针是正面进行渲染,顺时针是背面不渲染
        vertex_position = [
            (0, 0, 1),
            (1, 0, 1),
            (1, 0, 0),
            (0, 0, 1),
            (1, 0, 0),
            (0, 0, 0),
        ]
        texture_coord = [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 0),
            (1, 1),
            (1, 0),
        ]
        vertex_buffer_date = np.hstack([vertex_position, texture_coord]).astype(
            np.uint8
        )
        return vertex_buffer_date
