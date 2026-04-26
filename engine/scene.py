from typing import TYPE_CHECKING
from mesh.quardMesh import QuardMesh

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Scene:
    def __init__(self, engine: VoxelEngine):
        self.quard = QuardMesh(engine)

    def update(self):
        pass

    def render(self):
        self.quard.render()
