from typing import TYPE_CHECKING
import numpy as np
from mesh.baseMesh import BaseMesh

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine
    from world.chunk import Chunk


class ChunkMesh(BaseMesh):
    def __init__(self, chunk: Chunk):
        super().__init__(chunk.engine)
        self.sp = chunk.engine.shader_program_manage.chunk
        self.vbo_format = "3f 3f"
        self.vbo_attribution = ("in_position", "in_color")
        self.vao = self.getVAO()

    def getVertexBufferDate(self) -> np.ndarray:
        # 面剔除顶点逆时针是正面进行渲染,顺时针是背面不渲染
        vertices = [
            (-0.5, -0.5, 0),
            (0.5, -0.5, 0),
            (0.5, 0.5, 0),
            (0.5, 0.5, 0),
            (-0.5, 0.5, 0),
            (-0.5, -0.5, 0),
        ]
        color = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
        vertex_buffer_date = np.hstack([vertices, color], dtype=np.float32)
        return vertex_buffer_date
