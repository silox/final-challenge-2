from importlib import import_module
from os import listdir
import pygame
import random
import time

from constants import *
from level import Level
from misc_classes import FloorTransition, Timer


class App:
    APP_NAME = 'Final challenge 2.0'
    DEFAULT_BACKGROUND = 'resources/gfx/backgrounds/bg-default.png'

    def __init__(self):
        pygame.display.set_caption(self.APP_NAME)
        self.pg_screen = pygame.display.set_mode(RESOLUTION)
        self.quit = False
        self.debug = True
        self.current_level_id = 0
        self._timer = Timer()
        self.animation = FloorTransition(active=False)
        self.levels = []
        self.enabled_input_objects = set()
        self.current_level = None
        self.load_levels()

    def load_levels(self):
        '''Load every level{N}.py file into Level object'''
        for level_id, level_file_name in enumerate(sorted(filter(lambda name: name.endswith('.py'), listdir('levels')))):
            level_module = import_module(f'levels.{level_file_name[:-3]}')
            background = level_module.BACKGROUND if 'BACKGROUND' in dir(level_module) else self.DEFAULT_BACKGROUND
            music = level_module.MUSIC if 'MUSIC' in dir(level_module) else None
            level_object = Level(level_id, background, music, level_module.OBJECTS, self)
            self.levels.append(level_object)
        self.change_level(self.current_level_id)

    def change_level(self, level_id):
        if self.current_level is not None and self.current_level.level_id == level_id:
            return
        self.current_level = self.levels[self.current_level_id]
        if self.current_level.music is not None:
            pygame.mixer.music.load(self.current_level.music)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def move_screen(self, direction):
        new_level_id = direction + self.current_level_id
        if 0 <= new_level_id < len(self.levels):
            self.animation = FloorTransition(self.current_level, self.levels[new_level_id], direction)

    def handle_input(self):
        # Forbid input while animation is active
        for event in pygame.event.get():
            if self.animation.active:
                continue
            if event.type == pygame.QUIT:
                self.quit = True
            # handle input for every object in current level separately
            self.current_level.handle_event(event)

    def logic(self):
        # do transition between levels if animation is active
        self.animation.move(self)

        # change level if level_id is changed
        self.change_level(self.current_level_id)

        # do logic for every level object
        for obj in self.current_level.get_all_objects():
            if obj.active:
                obj.update()

    def render(self):
        self.current_level.background.draw(self.pg_screen)
        if self.animation.active:
            self.animation.new_level.background.draw(self.pg_screen)

        for obj in self.current_level.get_all_objects():
            if obj.visible:
                obj.draw(self.pg_screen)

        if self.animation.active:
            for obj in self.animation.new_level.get_all_objects():
                if obj.visible:
                    obj.draw(self.pg_screen)

    def increase_timer(self, seconds):
        self._timer.add(seconds)
        self._animate_timer_change(seconds)

    def decrease_timer(self, seconds):
        self.increase_timer(-seconds)

    def _animate_timer_change(self, seconds):
        color = RED if seconds < 0 else GREEN
        sign = '+' if seconds < 0 else '-'
        # TODO animation of added seconds


def main():
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 2, 1024)
    app = App()
    clock = pygame.time.Clock()
    while not app.quit:
        app.handle_input()
        app.logic()
        app.render()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
