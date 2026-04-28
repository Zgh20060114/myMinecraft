from typing import TYPE_CHECKING
from engine.settings import PLAYER_POS, PLAYER_SENSITIVITY, PLAYER_WALK_SPEED
from .camera import Camera
import pygame as pg

if TYPE_CHECKING:
    from engine.VoxelEngine import VoxelEngine


class Player(Camera):
    def __init__(
        self, engine: VoxelEngine, position=PLAYER_POS, pitch=0, yaw=-90
    ) -> None:
        super().__init__(position, pitch, yaw)
        self.engine = engine

    def update(self):
        self.mouseControl()
        self.keyboardControl()
        super().update()

    def mouseControl(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        # print(mouse_dx)
        if mouse_dx:
            self.rotateYaw(mouse_dx * PLAYER_SENSITIVITY)
        if mouse_dy:
            self.rotatePitch(mouse_dy * PLAYER_SENSITIVITY)

    def keyboardControl(self):
        key = pg.key.get_pressed()  # 列表,索引是键对应的数字
        velocity = PLAYER_WALK_SPEED * self.engine.delta_time
        if key[pg.K_w]:
            self.move_forward(velocity)
        if key[pg.K_s]:
            self.move_backward(velocity)
        if key[pg.K_a]:
            self.move_left(velocity)
        if key[pg.K_d]:
            self.move_right(velocity)
        if key[pg.K_q]:
            self.move_up(velocity)
        if key[pg.K_e]:
            self.move_down(velocity)
