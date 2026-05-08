from typing import TYPE_CHECKING
from engine.settings import CHUNK_SIZE
from mesh.chunkMesh import ChunkMesh
import glm


if TYPE_CHECKING:
    from world.world import World


class Chunk:
    def __init__(self, world: World, position=glm.ivec3(0, 0, 0)):
        self.position = position
        self.model_matrix = self.getModelMatrix()
        self.chunk_mesh = ChunkMesh(world, position)
        self.sp_chunk = self.chunk_mesh.sp

    def render(self):
        if not self.chunk_mesh.is_all_zero:
            self.setUniformsOnInit()
            self.chunk_mesh.render()

    def getModelMatrix(self):
        return glm.translate(glm.mat4(1.0), glm.vec3(self.position) * CHUNK_SIZE)

    def setUniformsOnInit(self):
        self.sp_chunk["m_model"].write(self.model_matrix)
