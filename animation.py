from itertools import chain
from random import randint

from window_constants import RESOLUTION, FPS

import pygame


pygame.mixer.init()


class FloorTransition:
    def __init__(self, old_level=None, new_level=None, direction=0, level_up=False, active=True, app=None):
        duration = 4 if level_up else 0.5
        assert RESOLUTION[1] % duration == 0 and FPS * duration < RESOLUTION[1]
        self.y_shift = RESOLUTION[1] // (duration * FPS)
        self.total_shift = 0
        self.direction = direction
        self.old_level = old_level
        self.active = active
        self.new_level = new_level
        self.app = app
        if level_up:
            pygame.mixer.music.load(f'resources/sfx/elevator/elevator{randint(1, 3)}.mp3')
            pygame.mixer.music.play()
        if old_level is not None and new_level is not None:
            for obj in new_level.get_all_objects():
                obj.move_coords(0, -RESOLUTION[1] * direction)
            new_level.background.y -= RESOLUTION[1] * direction
        if app is not None:
            app.global_objects['timer'].disable()

    def move(self, app=None):
        if not self.active:
            return
        if self.total_shift >= RESOLUTION[1]:
            # cleanup
            self.active = False
            if app is not None:
                app.current_level_id += self.direction
            for obj in self.old_level.get_all_objects():
                obj.move_coords(0, -self.total_shift * self.direction)
            self.old_level.background.y = 0
            self.total_shift = 0
            if self.app is not None:
                self.app.global_objects['timer'].enable()
        else:
            # moving
            self.old_level.background.move_coords(0, self.y_shift * self.direction)
            self.new_level.background.move_coords(0, self.y_shift * self.direction)
            for obj in chain(self.old_level.get_all_objects(), self.new_level.get_all_objects()):
                obj.move_coords(0, self.y_shift * self.direction)
            self.total_shift += self.y_shift


class MoveObjectAnimation:
    '''Move object to x, y in constant speed'''
    _SPEED = 2
    moving_objects = {}

    def __init__(self, gui_object, x, y, disappear=False, app=None):
        '''disappear only implemented for TextObject'''
        self.gui_object = gui_object
        self.x = x
        self.y = y
        self.start_x = gui_object.x
        self.start_y = gui_object.y
        self.app = app
        self.animation_id = 0 if not self.moving_objects else max(self.moving_objects.keys()) + 1
        self.moving_objects[self.animation_id] = self
        self.alpha = 255 if disappear else None
        self.app.disable_input = not disappear
    
    def move(self):
        self.gui_object.x += (self.x - self.start_x) / FPS * self._SPEED
        self.gui_object.y += (self.y - self.start_y) / FPS * self._SPEED

        if self.alpha is not None:
            self.alpha -= 255 / FPS * self._SPEED
            self.gui_object.update_text(alpha=self.alpha)

        if abs(self.start_x - self.x) <= abs(self.gui_object.x - self.start_x) \
            and abs(self.start_y - self.y) <= abs(self.gui_object.y - self.start_y):
            del self.moving_objects[self.animation_id] 
            self.gui_object.x = self.x
            self.gui_object.y = self.y
            self.app.disable_input = False
