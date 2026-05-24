from typing import TYPE_CHECKING
from world.world import World
from mesh.crossHairMesh import CrosshairMesh
from mesh.waterMesh import WaterMesh
import moderngl as mgl

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Scene:
    def __init__(self, engine: VoxelEngine):
        self.context = engine.context
        self.world = World(engine)
        self.crosshair = CrosshairMesh(engine)
        self.water = WaterMesh(engine)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()
        self.crosshair.render()
        self.context.disable(mgl.CULL_FACE)
        self.water.render()
        self.context.enable(mgl.CULL_FACE)
