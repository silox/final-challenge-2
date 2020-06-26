from importlib import import_module
from os import listdir
import pygame
import random
import sys
import time

from colors import Color
from global_objects import GLOBAL_OBJECTS
from level import Level
from animation import FloorTransition, MoveObjectAnimation
from window_constants import FPS, RESOLUTION


class App:
    APP_NAME = 'Final challenge 2: Kahoot is a lie!'
    DEFAULT_BACKGROUND = 'resources/gfx/backgrounds/bg-default.png'

    def __init__(self):
        pygame.display.set_caption(self.APP_NAME)
        self.pg_screen = pygame.display.set_mode(RESOLUTION)
        self.quit = False
        self.easy_mode = False
        self.argv1 = None if len(sys.argv) == 1 else sys.argv[1]
        self.current_level = None
        self.current_level_id = 0 if self.argv1 is None else 5
        self.current_highest_floor = self.current_level_id
        self.transition = FloorTransition(active=False)
        self.levels = []
        self.enabled_input_objects = set()
        self.disable_input = False
        self.global_objects = Level.create_gui_objects(GLOBAL_OBJECTS, self)
        self.load_levels()
        self.special_init()

    def load_levels(self):
        '''Load every level{N}.py file into Level object'''
        for level_id, level_file_name in enumerate(sorted(filter(lambda name: name.endswith('.py'), listdir('levels')))):
            level_module = import_module(f'levels.{level_file_name[:-3]}')
            background = level_module.BACKGROUND if 'BACKGROUND' in dir(level_module) else self.DEFAULT_BACKGROUND
            music = level_module.MUSIC if 'MUSIC' in dir(level_module) else None
            level_object = Level(level_id, background, music, level_module.OBJECTS, self)
            self.levels.append(level_object)
        self.change_level(self.current_level_id)

    def special_init(self):
        if self.current_level_id == 2:
            welcome_text_object = self.current_level.get_object('welcome_message').text
            welcome_text_object.update_text(welcome_text_object.text.replace('$', self.argv1))
        else:
            self.global_objects['timer'].disable()

    def change_level(self, level_id):
        if self.current_level is not None and self.current_level.level_id == level_id:
            return
        self.current_level = self.levels[self.current_level_id]
        App.change_music(self.current_level.music)

    @staticmethod
    def change_music(music_path=None):
        if music_path is None:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)

    def move_screen(self, direction):
        new_level_id = direction + self.current_level_id
        if 0 <= new_level_id < len(self.levels):
            is_new_floor = new_level_id > self.current_highest_floor
            self.transition = FloorTransition(self.current_level, self.levels[new_level_id], direction, level_up=is_new_floor, app=self)
            self.current_highest_floor = max(self.current_highest_floor, new_level_id)

    def handle_input(self):
        # Forbid input while transition is active
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            if self.transition.active or self.disable_input:
                continue

            # handle input for every object in current level
            for gui_object in self.current_level.get_all_objects():
                if self.enabled_input_objects and gui_object.obj_id not in self.enabled_input_objects:
                    continue
                if gui_object.reactive:
                    gui_object.handle_event(event)

            # handle input for all global objects
            for global_object in self.global_objects.values():
                if global_object.reactive:
                    global_object.handle_event(event)

    def logic(self):
        # do transition between levels if transition is active
        self.transition.move(self)

        # move all object that are supposed to move
        for moving_object in list(MoveObjectAnimation.moving_objects.values()):
            moving_object.move()

        # change level if level_id is changed
        self.change_level(self.current_level_id)

        # do logic for every level object
        for obj in self.current_level.get_all_objects():
            if obj.active:
                obj.update()
        
        # do logic for all global objects
        for global_object in self.global_objects.values():
            if global_object.active:
                global_object.update()
        
        # do some additional special logic
        self.special_logic()

    def special_logic(self, only_once_change=[True]):
        welcome_message = self.current_level.get_object('welcome_message')
        if welcome_message is not None and not welcome_message.visible and only_once_change[0]:
            self.global_objects['timer'].start()
            only_once_change[0] = False
        
        if self.current_level_id in (3, 5) and all(self.current_level.get_object(f'input_{i}').done for i in range(1, 5)):
            self.current_level.get_object('elevator_button_up').enabled = True

        if self.current_level_id == 5:
            if not random.randrange(30):
                self.current_level.get_object(f'ad_{random.randint(1, 4)}').enable()

    def render(self):
        self.current_level.background.draw(self.pg_screen)
        if self.transition.active:
            self.transition.new_level.background.draw(self.pg_screen)

        for obj in self.current_level.get_all_objects():
            if obj.visible:
                obj.draw(self.pg_screen)

        if self.transition.active:
            for obj in self.transition.new_level.get_all_objects():
                if obj.visible:
                    obj.draw(self.pg_screen)

        for global_object in self.global_objects.values():
            if global_object.visible:
                global_object.draw(self.pg_screen)


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
