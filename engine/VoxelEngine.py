from engine.settings import *
import pygame as pg
import moderngl as mgl
from engine.shaderProgram import ShaderProgram
from engine.scene import Scene
from engine.player import Player


class VoxelEngine:
    def __init__(self) -> None:
        pg.init()
        pg.font.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)  # 指定
        # pg.event.set_grab(True)
        # pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(WIN_SIZE, pg.OPENGL | pg.DOUBLEBUF)  # 创建
        self.font = pg.font.Font(None, 36)
        self.context = mgl.create_context()
        self.context.enable(
            mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND
        )  # 开启深度测试,面剔除cull, 透明混合
        self.context.gc_mode = "auto"  # 自动垃圾回收

        self.clock = pg.time.Clock()
        self.time = 0  # 游戏时间
        self.delta_time = 0  # 帧时间
        self.is_running = True

        self.player = Player(self)
        self.shader_program_manage = ShaderProgram(self)
        # self.shader_program_quard = self.shader_program_manage.getProgram("quard")
        # self.quard_mesh = QuardMesh(self)
        self.scene = Scene(self)

    def update(self):
        self.shader_program_manage.update()
        self.scene.update()
        self.player.update()
        self.delta_time = self.clock.tick(60)
        self.time = pg.time.get_ticks() / 1000
        # pg.display.set_caption(str(self.delta_time))
        # print(self.delta_time)
        self.fps = self.clock.get_fps()
        # print(self.fps)

    def render(self):
        self.context.clear(*BG_COLOR)  # 要清空吗
        self.scene.render()
        pg.display.flip()  # 交换整个缓冲区

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
