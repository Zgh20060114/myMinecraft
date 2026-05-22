from typing import TYPE_CHECKING
import pygame as pg
import moderngl as mgl

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Texture:
    def __init__(self, engine: VoxelEngine) -> None:
        self.context = engine.context
        self.texture_chunk = self.loadTexturePng("snow")
        self.texture_chunk.use(location=0)  # 绑定纹理插槽id
        self.texture_selected_box = self.loadTexturePng("frame")
        self.texture_selected_box.use(location=1)
        self.texture_array = self.loadTexturePng("tex_array_0", is_array=True)
        self.texture_array.use(location=2)

    def loadTexturePng(self, file_name, is_array=False):
        tex = pg.image.load(f"asset/{file_name}.png")
        # tex = pg.transform.flip(tex, False, True)
        if not is_array:
            texture = self.context.texture(
                tex.get_size(), 4, pg.image.tostring(tex, "RGBA", False), 0
            )
        else:
            layer_num = tex.get_height() // (tex.get_width() // 3)
            texture = self.context.texture_array(
                (tex.get_width(), tex.get_height() // layer_num, layer_num),
                4,
                pg.image.tostring(tex, "RGBA", False),
            )
        texture.anisotropy = 32
        texture.build_mipmaps()  # 粗调
        texture.filter = (mgl.NEAREST, mgl.NEAREST)  # 微调
        return texture
