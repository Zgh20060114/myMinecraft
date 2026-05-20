from glm import pos
from mesh.baseMesh import BaseMesh
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class SelectedBoxMesh(BaseMesh):
    def __init__(self, engine: "VoxelEngine"):
        super().__init__(engine)
        self.sp = engine.shader_program_manage.selected_box
        self.vbo_format = "3u1 2u1"
        self.vbo_attribution = ("in_position", "in_texture_coord")
        self.vao = self.getVAO()

    @staticmethod
    def makeData(position, index):
        data = []
        for trangle_index in index:
            for ind in trangle_index:
                data.append(position[ind])
        return data

    def getVertexBufferDate(self) -> np.ndarray:
        position_data = []
        texture_coord_data = []
        vertex_position = [
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (0, 1, 1),
            (0, 1, 0),
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
        ]
        vertex_index = [
            (0, 1, 2),
            (0, 2, 3),
            (5, 0, 3),
            (5, 3, 4),
            (3, 2, 7),
            (3, 7, 4),
            (6, 5, 4),
            (6, 4, 7),
            (1, 6, 7),
            (1, 7, 2),
            (5, 6, 1),
            (5, 1, 0),
        ]
        texture_position = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_index = [
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
        ]
        position_data = self.makeData(vertex_position, vertex_index)
        texture_coord_data = self.makeData(texture_position, texture_index)
        return np.hstack([position_data, texture_coord_data]).astype(np.uint8)
