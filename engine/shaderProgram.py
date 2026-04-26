class ShaderProgram:
    def __init__(self, engine) -> None:
        self.context = engine.context

    def getProgram(self, shader_name: str):
        with open(f"shader/{shader_name}.vert") as file:
            vert_file = file.read()
        with open(f"shader/{shader_name}.frag") as file:
            frag_file = file.read()
        shader_program = self.context.program(vert_file, frag_file)
        return shader_program

    # texture用的
    def setUniformsOnInit(self):
        pass

    def update(self):
        pass
