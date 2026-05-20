from typing import TYPE_CHECKING
import pygame as pg
import moderngl as mgl

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Texture:
    def __init__(self, engine: VoxelEngine) -> None:
        self.context = engine.context
        self.texture_chunk = self.loadTexturePng("snow")
        self.texture_chunk.use(location=0) # 绑定纹理插槽id
        self.texture_selected_box = self.loadTexturePng("frame")
        self.texture_selected_box.use(location=1)

    def loadTexturePng(self, file_name):
        tex = pg.image.load(f"asset/{file_name}.png")
        texture = self.context.texture(
            tex.get_size(), 4, pg.image.tostring(tex, "RGBA", False), 0
        )
        texture.anisotropy = 32
        texture.build_mipmaps()  # 粗调
        texture.filter = (mgl.NEAREST, mgl.NEAREST)  # 微调
        return texture
