from typing import TYPE_CHECKING
from world.chunk import Chunk

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Scene:
    def __init__(self, engine: VoxelEngine):
        self.chunk = Chunk(engine)

    def update(self):
        pass

    def render(self):
        self.chunk.render()
