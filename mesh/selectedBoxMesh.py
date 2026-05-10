from mesh.baseMesh import BaseMesh

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class SelectedBoxMesh(BaseMesh):
    def __init__(self, engine: "VoxelEngine"):
        super().__init__(engine)
        self.sp = engine.shader_program_manage.selected_box
        self.vbo_format = ""
