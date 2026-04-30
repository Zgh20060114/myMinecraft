from typing import TYPE_CHECKING
from engine.settings import CHUNK_SIZE
from mesh.chunkMesh import ChunkMesh
import glm

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Chunk:
    def __init__(self, engine: VoxelEngine, position=glm.vec3(0, 0, 0)):
        self.engine = engine
        self.position = position
        self.model_matrix = self.getModelMatrix()
        self.chunkMesh = ChunkMesh(self.engine)
        self.sp_chunk = self.chunkMesh.sp

    def render(self):
        self.setUniformsOnInit()
        self.chunkMesh.render()

    def getModelMatrix(self):
        return glm.translate(glm.mat4(1.0), self.position * CHUNK_SIZE)

    def setUniformsOnInit(self):
        self.sp_chunk["m_model"].write(self.model_matrix)
