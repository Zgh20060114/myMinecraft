from typing import TYPE_CHECKING
import numpy as np
from mesh.chunkMesh import ChunkMesh

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Chunk:
    def __init__(self, engine: VoxelEngine):
        self.engine = engine
        self.chunkMesh = ChunkMesh(self.engine)

    def render(self):
        self.chunkMesh.render()
