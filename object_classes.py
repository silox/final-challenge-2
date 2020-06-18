import pygame
from subprocess import Popen, PIPE, TimeoutExpired
import threading
import time
import webbrowser


from constants import *
from tasks import TASKS


pygame.init()


class GUIObject:
    '''Base class for every object in this app'''
    def __init__(self, x, y, width, height, obj_id=None, reactive=True, active=True, visible=True, app=None, name='', **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.obj_id = obj_id

        self.visible = visible
        self.active = active
        self.reactive = reactive

        self._app_instance = app
        self.name = name
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

    def enable(self):
        self.reactive = True
        self.active = True
        self.visible = True

    def disable(self):
        self.reactive = False
        self.active = False
        self.visible = False


class TextObject(GUIObject):
    def __init__(self, gui_options, text, color=BLACK, size=15, max_len=80, spacing=40, font='monospace', centered=True, **kwargs):
        font = pygame.font.SysFont(font, size)
        super().__init__(*gui_options, *font.size(text), **kwargs)
        self.fonts = [font.render(line, True, color) for line in self.divide_text(text, max_len)]
        self.rects = []
        self.spacing = spacing
        for i, font in enumerate(self.fonts):
            self.rects.append(font.get_rect())
            if not centered:
                self.rects[-1].center = self.x + self.width // 2, self.y + self.height // 2 + i * self.spacing
            else:
                self.rects[-1].center = self.x, self.y + i * self.spacing

    def draw(self, screen):
        for font, rect in zip(self.fonts, self.rects):
            screen.blit(font, rect)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        for rect in self.rects:
            rect_x, rect_y = rect.center
            rect.center = x + rect_x, y + rect_y

    @staticmethod
    def divide_text(text, max_len):
        text_list = text.split()
        result = ['']
        length = 0
        for i in range(len(text_list)):
            if length + len(result[-1]) > max_len:
                length = len(text_list[i])
                result[-1] = result[-1][:-1]
                result.append(text_list[i] + ' ')
            else:
                result[-1] += text_list[i] + ' '
        result[-1] = result[-1][:-1]
        return result


class ImageObject(GUIObject):
    def __init__(self, gui_options, image_path, scale=None, centered=False, **kwargs):
        self.img = pygame.image.load(image_path)
        if scale is not None:
            self.img = pygame.transform.smoothscale(self.img, scale)
        super().__init__(*gui_options, self.img.get_width(), self.img.get_height(), **kwargs)
        if centered:
            self.x -= self.img.get_width() // 2
            self.y -= self.img.get_height() // 2

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class InputObject(GUIObject):
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
        self.active_cursor = False
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
        self.max_letters = width // self.FONT_SIZE - 2
        self.idx_right = self.max_letters
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active_cursor = self.rect.collidepoint(event.pos)
            self.color = self.COLOR_ACTIVE if self.active_cursor else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.active_cursor:
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
        if self.active_cursor and self.ticks % 50 < 25:
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


class DialogueObject(GUIObject):
    DARK_SURFACE = pygame.Surface(RESOLUTION)
    BOX_BACKGROUND = (150, 50, 0)
    FONT = pygame.font.SysFont('Helvetica', 25, bold=True)

    def __init__(self, gui_options, text, enabled=False, **kwargs):
        super().__init__(*gui_options, **kwargs)
        if not enabled:
            self.disable()
        self.rect = pygame.Rect(*gui_options)
        self.surface = pygame.Surface(gui_options[2:])
        self.surface.fill(self.BOX_BACKGROUND)
        self.text = text
        self.clicked = False
        self.fonts = [self.FONT.render(txt, True, BLUE) for txt in TextObject.divide_text(text, self.width // 16)]
        self.DARK_SURFACE.set_alpha(200)
        x, y, width, _ = gui_options
        self.CLOSE_ICON = ImageObject((x + width - 45, y - 5), 'resources/gfx/misc/but-close.png')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.CLOSE_ICON.collision():
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.CLOSE_ICON.collision() and self.clicked and self.visible:
                self.disable()
                self._app_instance.enabled_input_objects.remove(self.obj_id)
            self.clicked = False

    def update(self):
        if self.visible:
            self._app_instance.enabled_input_objects.add(self.obj_id)

    def draw(self, screen):
        screen.blit(self.DARK_SURFACE, (0, 0))
        screen.blit(self.surface, (self.x, self.y))
        pygame.draw.rect(screen, WOODEN, self.rect, 4)
        self.CLOSE_ICON.draw(screen)
        for i, font in enumerate(self.fonts):
            text_coords = font.get_rect()
            text_coords.center = self.x + self.width // 2, self.y + (i + 1) * 25
            screen.blit(font, text_coords)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y
        self.CLOSE_ICON.move_coords(x, y)


class ButtonObject(GUIObject):
    CLICK_SOUND = pygame.mixer.Sound('resources/sfx/sounds/click.ogg')

    def __init__(self, gui_options, on_click, content=None, outline=BLUE, text_color=BLACK, **kwargs):
        super().__init__(*gui_options, **kwargs)
        self.content = self.create_content_object(content)
        self.rect = pygame.Rect(*gui_options)
        self.outline = outline
        self.prev_color = outline
        self.on_click = on_click
        self.clicked = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.clicked:
                self.CLICK_SOUND.play()
                self.on_click(self._app_instance)
            self.clicked = False

    def update(self):
        if self.content is not None:
            self.content.update()
        self.outline = BLACK if self.clicked else self.prev_color

    def draw(self, screen):
        if self.content is not None:
            self.content.draw(screen)
        pygame.draw.rect(screen, self.outline, self.rect, 2)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        if self.content is not None:
            self.content.move_coords(x, y)
        self.rect.x += x
        self.rect.y += y

    def create_content_object(self, object_dict):
        if object_dict is None:
            return None
        options_dict = {
            'gui_options': (self.x + self.width // 2, self.y + self.height // 2),
            'centered': True,
            **object_dict['options'],
        }
        if object_dict['type'] == 'image':
            options_dict['scale'] = (self.width, self.height)
        return object_type_dict[object_dict['type']](**options_dict)


class AdvertObject(GUIObject):
    def __init__(self, gui_options, image_path, url, **kwargs):
        self.content = ImageObject(gui_options, image_path)
        super().__init__(*gui_options, self.content.width, self.content.height, **kwargs)
        self.url = url
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.content.width, self.content.height)
        self.CLOSE_ICON = ImageObject((self.x + self.content.width - 45, self.y - 5), 'resources/gfx/misc/but-close.png')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.content.collision() and self.visible:
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
            if self.CLOSE_ICON.collision():
                self.disable()
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


class KahootAppObject(GUIObject):
    BUTTON_PATHS = [f'resources/gfx/kahoot/kahoot-{color}.png' for color in ('red', 'blue', 'green', 'yellow')]
    BUTTON_OPTIONS = [
        (RESOLUTION[0] // 4, RESOLUTION[1] // 4 * 3 - 40), (RESOLUTION[0] // 4 * 3, RESOLUTION[1] // 4 * 3 - 40),
        (RESOLUTION[0] // 4, RESOLUTION[1] // 4 * 3 + 100), (RESOLUTION[0] // 4 * 3, RESOLUTION[1] // 4 * 3 + 100),
    ]

    class Question:
        IMAGE_OPTIONS = (RESOLUTION[0] // 2, RESOLUTION[1] // 2 - 100)
        QUESTION_TEXT_OPTIONS = (RESOLUTION[0] // 2, 50)

        def __init__(self, question, answers, correct, image=None):
            self.question_text = TextObject(self.QUESTION_TEXT_OPTIONS, question, size=30, font='Helvetica', visible=False)
            self.answers = []
            for options, answer in zip(KahootAppObject.BUTTON_OPTIONS, answers):
                if len(answer) > 30:
                    options = (options[0], options[1] - 40)
                self.answers.append(TextObject(options, answer, color=WHITE, size=20, max_len=30, spacing=20, font='Helvetica'))
            self.correct = correct
            self.image = None if image is None else ImageObject(self.IMAGE_OPTIONS, image, centered=True, visible=False)

        def draw(self, screen):
            if self.image is not None:
                self.image.draw(screen)
            self.question_text.draw(screen)
            for answer in self.answers:
                answer.draw(screen)

        def select(self, user_answer):
            return user_answer == self.correct

    def __init__(self, questions, **kwargs):
        super().__init__(*(0,) * 4, **kwargs)
        self.questions = [self.Question(**question) for question in questions]
        self.buttons = [ImageObject(options, path, scale=(450, 120), centered=True) for options, path in zip(self.BUTTON_OPTIONS, self.BUTTON_PATHS)]
        self.current_question = -1
        self.clicked_id = 0
        self.clicked = False

    def start(self):
        self.current_question = 0
        self.enable()

    def handle_event(self, event):
        if self.current_question == -1:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, button in enumerate(self.buttons):
                if button.collision():
                    self.clicked = True
                    self.clicked_id = i

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
            for i, button in enumerate(self.buttons):
                if button.collision() and i == self.clicked_id:
                    if self.questions[self.current_question].select(self.clicked_id):
                        self.current_question += 1
                    else:
                        self._app_instance.increase_timer(120)
                        self.return_back()
                    break
            self.clicked = False

    def update(self):
        # Last question is correct
        if self.current_question == len(self.questions):
            self.return_back()
            self._app_instance.current_level.get_object('elevator_button_up').enabled = True

    def draw(self, screen):
        if self.current_question == -1:
            return

        for button in self.buttons:
            button.draw(screen)
        self.questions[self.current_question].draw(screen)

    def return_back(self):
        self.current_question = -1
        for gui_object in self._app_instance.current_level.get_all_objects():
            if gui_object.name != 'instructions_dialogue':
                gui_object.enable()


class TaskPanelObject(GUIObject):
    PANEL_PATH = 'resources/gfx/task-panel/panel.png'

    class Task:
        TIMEOUT = 4

        def __init__(self, task_name, task_text, time_limit, tests):
            self.name = task_name
            self.text = task_text
            self.time_limit = time_limit
            self.tests = tests

        def submit(self, parent):
            start_time = time.time()
            for test_input, correct_output in self.tests:
                try:
                    for cmd in 'python', 'python3':
                        process = Popen([cmd, f'submits/{self.name}.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                        user_output, _ = process.communicate(input=test_input, timeout=self.TIMEOUT)
                        if not process.returncode:
                            break
                    else:
                        parent.result = 'EXC'
                        return
                except TimeoutExpired:
                    process.kill()
                    parent.result = 'TLE'
                    return
                except Exception as exc:
                    print(exc)
                    parent.result = 'ERR'
                    return
                if user_output != correct_output + '\n':
                    parent.result = 'WA'
                    return
                if time.time() - start_time > self.time_limit:
                    parent.result = 'TLE'
                    return
            parent.result = 'OK'

    def __init__(self, centered=True, **kwargs):
        x_mid, y_mid = RESOLUTION[0] // 2, RESOLUTION[1] // 2
        self.panel = ImageObject((x_mid, y_mid), self.PANEL_PATH, scale=(300, 500), centered=centered)
        super().__init__(self.panel.x, self.panel.y, self.panel.width, self.panel.height, **kwargs)
        self.button_task = ImageObject((x_mid, y_mid - 120), 'resources/gfx/task-panel/task-button.png', centered=True, scale=(200, 80))
        self.button_submit = ImageObject((x_mid, y_mid - 20), 'resources/gfx/task-panel/submit-button.png', centered=True, scale=(200, 80))
        self.elevator_button = ImageObject((x_mid, y_mid + 190), 'resources/gfx/elevator/elevator-down.png', centered=True, scale=(50, 50))
        self.elevator_button.disable()
        self.panel_top = ImageObject((x_mid, y_mid + 190), 'resources/gfx/task-panel/panel-top.png', centered=True, scale=(100, 100))
        self.left_arrow = ImageObject((x_mid - 140, y_mid - 230), 'resources/gfx/task-panel/left-arrow.png', scale=(50, 50))
        self.right_arrow = ImageObject((x_mid + 90, y_mid - 230), 'resources/gfx/task-panel/right-arrow.png', scale=(50, 50))
        self.current_task = 0
        self.result = None
        self.tasks = [self.Task(*task) for task in TASKS]
        self.dialogues = [DialogueObject((150, 200, 700, 300), task.text, obj_id=self.obj_id, app=self._app_instance) for task in self.tasks]

    def handle_event(self, event):
        if self.dialogues[self.current_task].reactive:
            self.dialogues[self.current_task].handle_event(event)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_submit.collision():
                thread = threading.Thread(target=self.tasks[self.current_task].submit, args=[self])
                thread.start()
            elif self.button_task.collision():
                self.dialogues[self.current_task].enable()
            elif self.elevator_button.reactive and self.elevator_button.collision():
                self.elevator_button.disable()
                self._app_instance.current_level.get_object('elevator_button_down').enable()
            elif self.left_arrow.reactive and self.left_arrow.collision():
                self.current_task -= 1
            elif self.right_arrow.reactive and self.right_arrow.collision():
                self.current_task += 1

    def update(self):
        if self.result == 'OK':
            self.panel_top.disable()
            self.elevator_button.enable()

        if self.dialogues[self.current_task].active:
            self.dialogues[self.current_task].update()

        if self.current_task != 0:
            self.left_arrow.enable()
        else:
            self.left_arrow.disable()
        if self.current_task != len(self.tasks) - 1:
            self.right_arrow.enable()
        else:
            self.right_arrow.disable()

    def draw(self, screen):
        self.panel.draw(screen)
        if self.result is not None:
            #self.result_text_object.draw(screen)
            print(self.result)
            self.result = None
        
        if self.elevator_button.visible:
            self.elevator_button.draw(screen)
        if self.panel_top.visible:
            self.panel_top.draw(screen)
        
        if self.button_submit.visible:
            self.button_submit.draw(screen)
        if self.button_task.visible:
            self.button_task.draw(screen)

        if self.left_arrow.visible:
            self.left_arrow.draw(screen)
        if self.right_arrow.visible:
            self.right_arrow.draw(screen)

        if self.dialogues[self.current_task].visible:
            self.dialogues[self.current_task].draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.panel.move_coords(x, y)
        self.dialogues[self.current_task].move_coords(x, y)
        self.button_task.move_coords(x, y)
        self.button_submit.move_coords(x, y)
        self.elevator_button.move_coords(x, y)
        self.panel_top.move_coords(x, y)
        self.left_arrow.move_coords(x, y)
        self.right_arrow.move_coords(x, y)


class ChangeLevelObject(GUIObject):
    def __init__(self, gui_options, direction, enabled=None, **kwargs):
        self.img_enabled = ImageObject(gui_options, f'resources/gfx/elevator/elevator-{direction}.png')
        self.img_disabled = ImageObject(gui_options, f'resources/gfx/elevator/elevator-{direction}-dis.png')
        self.img_lightened = ImageObject(gui_options, f'resources/gfx/elevator/elevator-{direction}-light.png')
        super().__init__(*gui_options, self.img_enabled.img.get_width(), self.img_enabled.img.get_height(), **kwargs)
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
                assert self._app_instance is not None, 'ChangeLevelObject does not have its app attached'
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
    'dialogue': DialogueObject,
    'image': ImageObject,
    'input': InputObject,
    'kahoot': KahootAppObject,
    'level_changer': ChangeLevelObject,
    'task_panel': TaskPanelObject,
    'text': TextObject,
}
