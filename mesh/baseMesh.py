from typing import TYPE_CHECKING
from moderngl import VertexArray
import numpy as np

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class BaseMesh:
    def __init__(self, engine: "VoxelEngine"):
        self.context = engine.context
        self.sp = None
        self.vbo_format: str = ""
        self.vbo_attribution: tuple[str, ...] = ()
        self.vao = None

    def getVertexBufferDate(self) -> np.ndarray: ...

    def getVAO(self) -> VertexArray:
        vbd = self.getVertexBufferDate()
        buffer = self.context.buffer(vbd)  # 把cpu上的vbd搬运到gpu上
        vao = self.context.vertex_array(
            self.sp, [(buffer, self.vbo_format, *self.vbo_attribution)]
        )
        return vao

    def render(self):
        self.vao.render()
