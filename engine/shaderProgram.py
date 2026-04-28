from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class ShaderProgram:
    def __init__(self, engine: VoxelEngine) -> None:
        self.context = engine.context
        self.player = engine.player
        self.chunk = self.getProgram("chunk")
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

    def update(self):
        self.chunk["m_view"].write(self.player.view_matrix)
