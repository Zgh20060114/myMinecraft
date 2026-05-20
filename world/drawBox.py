from mesh.selectedBoxMesh import SelectedBoxMesh
from world.voxelSelect import VoxelSelect
import glm


class DrawBox:
    def __init__(self, voxelSelect: VoxelSelect) -> None:
        self.selector = voxelSelect
        self.engine = self.selector.engine
        self.position = glm.vec3(0)
        # self.m_model = glm.mat4(0)
        self.selected_box = voxelSelect.engine.shader_program_manage.selected_box
        self.box_mesh = SelectedBoxMesh(self.engine)

    def update(self):
        if self.selector.selected_voxel_id:
            self.position = self.selector.selected_voxel_world_pos

    def getModelMatrix(self):
        return glm.translate(glm.mat4(1.0), glm.vec3(self.position))

    def setUniform(self):
        self.selected_box["m_model"].write(self.getModelMatrix())

    def render(self):
        if self.selector.selected_voxel_id:
            self.setUniform()
            self.box_mesh.render()
