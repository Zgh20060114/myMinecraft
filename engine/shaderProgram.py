from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class ShaderProgram:
    def __init__(self, engine: VoxelEngine) -> None:
        self.context = engine.context
        self.player = engine.player
        self.texture_manage = engine.texture_manage
        self.chunk = self.getProgram("chunk")
        self.selected_box = self.getProgram("selectedBox")
        self.setUniformsOnInit()

    def getProgram(self, shader_name: str):
        with open(f"shader/{shader_name}.vert") as file:
            vert_file = file.read()
        with open(f"shader/{shader_name}.frag") as file:
            frag_file = file.read()
        shader_program = self.context.program(vert_file, frag_file)
        return shader_program

    # 设置统一变量uniform用的
    def setUniformsOnInit(self):
        self.chunk["m_view"].write(self.player.view_matrix)
        self.chunk["m_projection"].write(self.player.projection_matrix)
        self.chunk["m_model"].write(self.player.model_matrix)
        self.chunk["texture_chunk"].value = 0  # modenGL,必须和frag中的名称对上
        self.chunk["texture_selected_box"].value = 1

    def update(self):
        self.chunk["m_view"].write(self.player.view_matrix)
