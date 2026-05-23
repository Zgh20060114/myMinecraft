from typing import TYPE_CHECKING
from world.world import World
from mesh.crossHairMesh import CrosshairMesh

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Scene:
    def __init__(self, engine: VoxelEngine):
        self.world = World(engine)
        self.crosshair = CrosshairMesh(engine)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()
        self.crosshair.render()
