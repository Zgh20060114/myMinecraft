from typing import TYPE_CHECKING
from world import world
from world.world import World

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Scene:
    def __init__(self, engine: VoxelEngine):
        self.world = World(engine)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()
