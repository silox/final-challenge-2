import pygame
import webbrowser

from constants import *


pygame.init()


class GUIObject:
    '''Base class for every object in this app'''
    def __init__(self, x, y, width, height, obj_id=None, visible=True,
                 active=False, hover_cursor='arrow', app=None, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.obj_id = obj_id
        self.visible = visible
        self.active = active
        self.hover_cursor = hover_cursor

        self._app_instance = app
        self.kwargs = kwargs

    def handle_event(self, event):
        '''Method to be overriden'''
        pass

    def update(self):
        '''Method to be overriden'''
        pass

    def draw(self, screen):
        '''Method to be overriden'''
        pass

    def move_coords(self, x, y):
        self.x += x
        self.y += y

    def collision(self):
        x, y = pygame.mouse.get_pos()
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height


class TextObject(GUIObject):
    def __init__(self, gui_options, text, color=BLACK, size=15, font='monospace', **kwargs):
        super().__init__(*gui_options, **kwargs)
        font = pygame.font.SysFont(font, size)
        self.font = font.render(text, True, color)
        rect = self.font.get_rect()
        rect.center = self.x + self.width // 2, self.y + self.height // 2

        self.text = text
        self.color = color

    def draw(self, screen):
        screen.blit(self.font, (self.x, self.y))


class ImageObject(GUIObject):
    def __init__(self, gui_options, image_path, scale=None, visible=True, **kwargs):
        self.img = pygame.image.load(image_path)
        if scale is not None:
            self.img = pygame.transform.scale(self.img, scale)
        x, y, _, _ = gui_options
        super().__init__(x, y, self.img.get_width(), self.img.get_height(), visible=visible, **kwargs)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class InputBox(GUIObject):
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    COMFY_CONSTANT = 20
    FONT_SIZE = 10
    TEXT_SIZE = 16
    MAXLEN = 200

    def __init__(self, gui_options, task, answer, correct='Correct answer', wrong='Wrong answer',
                 initial_text='', synonyms=None, **kwargs):
        super().__init__(*gui_options, **kwargs)
        x, y, width, height = gui_options
        self.rect = pygame.Rect(*gui_options)
        self.FONT = pygame.font.SysFont('monospace', self.TEXT_SIZE)
        self.font = self.FONT.render(initial_text, True, BLACK)
        self.bottom_text = self.FONT.render('', True, RED)
        self.above_text = self.FONT.render(task, True, BLACK)
        self.color = self.COLOR_INACTIVE
        self.synonyms = set() if synonyms is None else set(synonyms)
        self.answer = answer
        self.correct = correct
        self.task = task
        self.text = initial_text
        self.wrong = wrong
        self.action_text = ''
        self.event_char = ''
        self.comfy_timer = 0
        self.idx = 0
        self.task_done = 0
        self.ticks = 0
        self.idx_left = 0
        self.max_letters =  width // self.FONT_SIZE - 2
        self.idx_right = self.max_letters
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.done = self.text.lower() == self.answer or self.text.lower() in self.synonyms
                text, color = (self.correct, GREEN) if self.done else (self.wrong, RED)
                self.bottom_text = self.FONT.render(text, True, color)
                self.text = ''
                self.idx = 0
                self.idx_left = 0
                self.idx_right = self.max_letters
            elif event.key == pygame.K_BACKSPACE:
                self._backspace_text()
            elif event.key == pygame.K_DELETE:
                self._del_text()
            elif event.key == pygame.K_LEFT:
                self._left_cursor()
            elif event.key == pygame.K_RIGHT:
                self._right_cursor()
            elif len(self.text) < self.MAXLEN and ' ' <= event.unicode <= '~':
                self._insert_text(event.unicode)
            self.font = self.FONT.render(self.text[self.idx_left:self.idx_right], True, self.color)
        if event.type == pygame.KEYUP:
            self.event_char = ''
            self.action_text = ''

    def update(self):
        self.comfy_timer = self.comfy_timer + 1 if self.event_char else 0
        # After 20 ticks start deleting text
        if self.comfy_timer % self.COMFY_CONSTANT == 0:
            self.action_text = self.event_char
        # Delete text every 2 ticks
        if self.action_text and self.comfy_timer % 2 == 0:
            if self.action_text == 'backspace':
                self._backspace_text()
            elif self.action_text == 'del':
                self._del_text()
            elif self.action_text == 'left':
                self._left_cursor()
            elif self.action_text == 'right':
                self._right_cursor()
            elif len(self.text) < self.MAXLEN and ' ' <= self.event_char <= '~':
                self._insert_text(self.event_char)
            self.font = self.FONT.render(self.text[self.idx_left:self.idx_right], True, self.color)
        self.ticks = 5 if self.comfy_timer or self.event_char else self.ticks + 1

    def draw(self, screen):
        screen.blit(self.font, (self.rect.x + self.height // 2 - self.FONT_SIZE, self.rect.y + self.height // 4))
        bottom_text_coords = self.bottom_text.get_rect()
        bottom_text_coords.center = self.x + self.width // 2, self.y + self.height + 20
        screen.blit(self.bottom_text, bottom_text_coords)
        above_text_coords = self.above_text.get_rect()
        above_text_coords.center = self.x + self.width // 2, self.y - 20
        screen.blit(self.above_text, above_text_coords)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.active and self.ticks % 50 < 25:
            cursor_x = (self.x + (self.idx + 1) * self.FONT_SIZE) - self.FONT_SIZE // 2 + 1
            pygame.draw.line(screen, BLACK, (cursor_x, self.y + self.height // 4), (cursor_x, self.y + int(self.height * 0.75)), 2)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y

    def _insert_text(self, char):
        self.text = self.text[:self.idx_left + self.idx] + char + self.text[self.idx_left + self.idx:]
        self._shift_index(1)
        self.event_char = char

    def _backspace_text(self):
        if self.idx_left == self.idx == 0:
            return
        self.text = self.text[:self.idx_left + self.idx - 1] + self.text[self.idx_left + self.idx:]
        if self.idx_left != 0:
            self.idx_left -= 1
            self.idx_right -= 1
        elif self.idx != 0:
            self.idx -= 1
        self.event_char = 'backspace'

    def _del_text(self):
        self.text = self.text[:self.idx_left + self.idx] + self.text[self.idx_left + self.idx + 1:]
        self.event_char = 'del'

    def _left_cursor(self):
        self._shift_index(-1)
        self.event_char = 'left'

    def _right_cursor(self):
        self._shift_index(1)
        self.event_char = 'right'

    def _shift_index(self, n):
        if 0 <= self.idx + n <= self.max_letters and self.idx + n <= len(self.text):
            self.idx += n
        elif self.idx_left + n >= 0 and self.idx_right + n <= len(self.text):
            self.idx_left += n
            self.idx_right += n


class DialogueBox(GUIObject):
    DARK_SURFACE = pygame.Surface(RESOLUTION)
    BOX_BACKGROUND = (150, 50, 0)
    FONT = pygame.font.SysFont('Helvetica', 25, bold=True)

    def __init__(self, gui_options, text='', **kwargs):
        super().__init__(*gui_options, **kwargs)
        self.rect = pygame.Rect(*gui_options)
        self.surface = pygame.Surface(gui_options[2:])
        self.surface.fill(self.BOX_BACKGROUND)
        self.text = text
        self.clicked = False
        self.fonts = [self.FONT.render(txt, True, BLUE) for txt in DialogueBox.divide_text(text)]
        self.DARK_SURFACE.set_alpha(200)
        x, y, width, _ = gui_options
        self.CLOSE_ICON = ImageObject((x + width - 45, y - 5, width, self.height), 'resources/gfx/but-close.png')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.CLOSE_ICON.collision():
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.CLOSE_ICON.collision() and self.clicked and self.visible:
                self.visible = False
                self._app_instance.enabled_input_objects.remove(self.obj_id)
            self.clicked = False

    def draw(self, screen):
        screen.blit(self.DARK_SURFACE, (0, 0))
        screen.blit(self.surface, (self.x, self.y))
        pygame.draw.rect(screen, WOODEN, self.rect, 4)
        self.CLOSE_ICON.draw(screen)
        for i, font in enumerate(self.fonts):
            text_coords = font.get_rect()
            text_coords.center = self.x + self.width // 2, self.y + (i + 1) * 25
            screen.blit(font, text_coords)

    def update(self):
        if self.visible:
            self._app_instance.enabled_input_objects.add(self.obj_id)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y
        self.CLOSE_ICON.move_coords(x, y)

    @staticmethod
    def divide_text(text):
        p = text.split()
        ret = [""]
        s = 0
        for i in range(len(p)):
            if s + len(ret[-1]) > 30:
                s = len(p[i])
                ret[-1] = ret[-1][:-1]
                ret.append(p[i] + " ")
            else:
                ret[-1] += p[i] + " "
        ret[-1] = ret[-1][:-1]
        return ret


class ButtonObject(GUIObject):
    FONT = pygame.font.SysFont('Times New Roman', 30)
    CLICK_SOUND = pygame.mixer.Sound('resources/sfx/click.ogg')

    def __init__(self, gui_options, on_click, bg_color, text_color, content, *args, **kwargs):
        super().__init__(*gui_options, **kwargs)
        self.content = create_content_object(content)
        self.rect = pygame.Rect(*gui_options)
        self.bg_color = bg_color
        self.prev_color = self.bg_color
        self.on_click = on_click
        self.clicked = False
        self.args = args
        self.kwargs = kwargs

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.clicked:
                self.SFX.play()
                self.on_click(*self.args, **self.kwargs)
            self.clicked = False

    def update(self):
        self.bg_color = BLACK if self.clicked else self.prev_color

    def draw(self, screen):
        self.content.draw(screen)
        pygame.draw.rect(screen, self.bg_color, self.rect, 2)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.content.move_coords(x, y)
        self.rect.x += x
        self.rect.y += y

    @staticmethod
    def create_content_object(object_dict):
        return object_type_dict[object_dict['type']](**object_dict['options'])


class AdvertObject(GUIObject):
    def __init__(self, gui_options, image_path, url, **kwargs):
        super().__init__(*gui_options, **kwargs)
        self.content = ImageObject(gui_options, image_path)
        self.url = url
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.content.width, self.content.height)
        self.CLOSE_ICON = ImageObject((self.x + self.content.width - 45, self.y - 5, self.content.width, self.content.height), 'resources/gfx/but-close.png')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.content.collision() and self.visible:
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
            if self.CLOSE_ICON.collision():
                self.visible = False
            elif self.content.collision() and self.visible:
                webbrowser.open(self.url)
            self.clicked = False

    def draw(self, screen):
        self.content.draw(screen)
        pygame.draw.rect(screen, WOODEN, self.rect, 5)
        self.CLOSE_ICON.draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y
        self.content.move_coords(x, y)
        self.CLOSE_ICON.move_coords(x, y)


class ChangeLevelObject(GUIObject):
    def __init__(self, gui_options, direction, enabled=None, **kwargs):
        self.img_enabled = ImageObject(gui_options, f'resources/gfx/elevator-{direction}.png')
        self.img_disabled = ImageObject(gui_options, f'resources/gfx/elevator-{direction}-dis.png')
        self.img_lightened = ImageObject(gui_options, f'resources/gfx/elevator-{direction}-light.png')
        x, y, _, _ = gui_options
        super().__init__(x, y, self.img_enabled.img.get_width(), self.img_enabled.img.get_height(), **kwargs)
        self.clicked = False
        self.direction = direction
        self.enabled = enabled if enabled is not None else True if direction == 'down' else False
        self.changer = 1 if direction == 'up' else -1

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.img_enabled.collision():
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.img_enabled.collision() and self.clicked and self.enabled and self.visible:
                assert self._app_instance is not None, 'NextLevelObject does not have its app attached'
                self._app_instance.move_screen(self.changer)
            self.clicked = False

    def draw(self, screen):
        if self.enabled and self.clicked and self.img_lightened.collision():
            self.img_lightened.draw(screen)
        elif self.enabled:
            self.img_enabled.draw(screen)
        else:
            self.img_disabled.draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.img_lightened.move_coords(x, y)
        self.img_enabled.move_coords(x, y)
        self.img_disabled.move_coords(x, y)


object_type_dict = {
    'object': GUIObject,
    'advert': AdvertObject,
    'button': ButtonObject,
    'dialogue_box': DialogueBox,
    'image': ImageObject,
    'input_box': InputBox,
    'level_changer': ChangeLevelObject,
    'text': TextObject,
}
