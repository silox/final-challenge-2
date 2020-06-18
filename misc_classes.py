from itertools import chain

from constants import *


class FloorTransition:
    def __init__(self, old_level=None, new_level=None, direction=0, duration=0.5, active=True):
        assert RESOLUTION[1] % duration == 0 and FPS * duration < RESOLUTION[1]
        self.y_shift = RESOLUTION[1] // (duration * FPS)
        self.total_shift = 0
        self.direction = direction
        self.old_level = old_level
        self.active = active
        self.new_level = new_level
        if old_level is not None and new_level is not None:
            for obj in new_level.get_all_objects():
                obj.move_coords(0, -RESOLUTION[1] * direction)
            new_level.background.y -= RESOLUTION[1] * direction

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
        else:
            # moving
            self.old_level.background.move_coords(0, self.y_shift * self.direction)
            self.new_level.background.move_coords(0, self.y_shift * self.direction)
            for obj in chain(self.old_level.get_all_objects(), self.new_level.get_all_objects()):
                obj.move_coords(0, self.y_shift * self.direction)
            self.total_shift += self.y_shift


class Timer:
    # TODO
    def __init__(self):
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def add(self, seconds):
        self.seconds += seconds
