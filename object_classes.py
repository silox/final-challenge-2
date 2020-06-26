import pygame
from subprocess import Popen, PIPE, TimeoutExpired
import threading
import time
import webbrowser

from animation import MoveObjectAnimation
from colors import Color
from tasks import TASKS
from window_constants import FPS, RESOLUTION


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
    '''gui_options - (x, y)'''
    def __init__(self, gui_options, text, color=Color.black, size=15, max_len=80, spacing=40,
                 font='monospace', centered=True, **kwargs):
        self.font = pygame.font.SysFont(font, size)
        super().__init__(*gui_options, *self.font.size(text), **kwargs)
        self.color = color
        self.text = text
        self.max_len = max_len
        self.spacing = spacing
        self.centered = centered
        self.update_text(text, color)

    def update_text(self, text=None, color=None, alpha=None):
        if color is not None:
            self.color = color
        if text is not None:
            self.text = text
        if alpha is not None:
            self._fonts = [self.font.render(line, True, self.color, self.color) for line in self.divide_text(self.text, self.max_len)]
            for font in self._fonts:
                font.set_colorkey(self.color)
                font.set_alpha(alpha)
        else:
            self._fonts = [self.font.render(line, True, self.color) for line in self.divide_text(self.text, self.max_len)]
        self.rects = []
        for i, font in enumerate(self._fonts):
            self.rects.append(font.get_rect())
            if not self.centered:
                self.rects[-1] = self.rects[-1].move(self.x, self.y + i * self.spacing)
            else:
                self.rects[-1].center = self.x, self.y + i * self.spacing

    def draw(self, screen):
        if self.visible:
            for font, rect in zip(self._fonts, self.rects):
                screen.blit(font, rect)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        for rect in self.rects:
            rect_x, rect_y = rect.center
            rect.center = x + rect_x, y + rect_y

    def get_number_of_lines(self):
        return len(self._fonts)

    @staticmethod
    def divide_text(text, max_len):
        result = []
        current = ''
        for word in text.split():
            if len(word) + len(current) > max_len:
                result.append(current[:-1])
                current = word + ' '
            else:
                current += word + ' '
        return result + [current[:-1]]


class ImageObject(GUIObject):
    '''gui_options - (x, y)'''
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
    '''gui_options - (x, y, width, height)'''
    COMFY_CONSTANT = 20
    FONT_SIZE = 10
    TEXT_SIZE = 16
    MAXLEN = 200

    def __init__(self, gui_options, task, answer, correct='Correct answer', wrong='Wrong answer',
                 initial_text='', synonyms=None, bold=False, reward=0, **kwargs):
        super().__init__(*gui_options, **kwargs)
        x, y, width, height = gui_options
        self.rect = pygame.Rect(*gui_options)
        self.FONT = pygame.font.SysFont('monospace', self.TEXT_SIZE, bold=bold)
        self.font = self.FONT.render(initial_text, True, Color.black)
        self.task_text = TextObject((self.x + self.width // 2, self.y - 40), task, centered=True, size=self.TEXT_SIZE, max_len=40, spacing=15)
        self.bottom_text = TextObject((self.x + self.width // 2, self.y + 50), '', color=Color.red, centered=True, size=self.TEXT_SIZE, max_len=40, spacing=15)
        self.color = Color.inactive
        self.synonyms = set() if synonyms is None else set(synonyms)
        self.answer = answer
        self.active_cursor = False
        self.correct = correct
        self.task = task
        self.text = initial_text
        self.wrong = wrong
        self.reward = reward
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
            self.color = Color.active if self.active_cursor else Color.inactive
        if event.type == pygame.KEYDOWN and self.active_cursor:
            if event.key == pygame.K_RETURN:
                if self.text.lower() == self.answer or self.text.lower() in self.synonyms and not self.done:
                    self._app_instance.global_objects['timer'].decrease(seconds=self.reward)
                    self.done = True
                text, color = (self.correct, Color.success) if self.done else (self.wrong, Color.red)
                self.bottom_text.update_text(text=text, color=color)
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
        screen.blit(self.font, (self.rect.x + self.FONT_SIZE, self.rect.y + self.height // 4))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        self.task_text.draw(screen)
        self.bottom_text.draw(screen)
        if self.active_cursor and self.ticks % 50 < 25:
            cursor_x = (self.x + 4 + (self.idx + 1) * self.FONT_SIZE) - self.FONT_SIZE // 2 + 1
            pygame.draw.line(screen, Color.black, (cursor_x, self.y + self.height // 4), (cursor_x, self.y + int(self.height * 0.75)), 2)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y
        self.task_text.move_coords(x, y)
        self.bottom_text.move_coords(x, y)

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


class MessageObject(GUIObject):
    '''gui_options - (x, y, width)'''
    DARK_SURFACE = pygame.Surface(RESOLUTION)
    FONT = pygame.font.SysFont('Helvetica', 25, bold=True)

    def __init__(self, gui_options, text, text_color=Color.white, enabled=False, **kwargs):
        x, y, width = gui_options
        self.text = TextObject((x + 30, y + 75), text, color=text_color, max_len=width // 14, spacing=25,
                               font='Helvetica', size=25, bold=True, centered=False)
        height = self.text.get_number_of_lines() * 25 + 100
        super().__init__(x, y, width, height, **kwargs)  # Add empty height
        if not enabled:
            self.disable()
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.surface.fill(Color.chocolate)
        self.clicked = False
        self.DARK_SURFACE.set_alpha(200)
        self.CLOSE_ICON = ImageObject((x + width - 55, y + 5), 'resources/gfx/misc/but-close.png')

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
        pygame.draw.rect(screen, Color.wooden, self.rect, 4)
        self.CLOSE_ICON.draw(screen)
        self.text.draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y
        self.CLOSE_ICON.move_coords(x, y)
        self.text.move_coords(x, y)


class ButtonObject(GUIObject):
    '''gui_options - (x, y, width, height)'''
    CLICK_SOUND = pygame.mixer.Sound('resources/sfx/sounds/click.ogg')

    def __init__(self, gui_options, on_click, content=None, outline=Color.blue, text_color=Color.black, **kwargs):
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
        self.outline = Color.black if self.clicked else self.prev_color

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
    '''gui_options - (x, y)'''
    def __init__(self, gui_options, image_path, url, **kwargs):
        self.content = ImageObject(gui_options, image_path, scale=(400, 300))
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
        pygame.draw.rect(screen, Color.wooden, self.rect, 5)
        self.CLOSE_ICON.draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.rect.x += x
        self.rect.y += y
        self.content.move_coords(x, y)
        self.CLOSE_ICON.move_coords(x, y)


class KahootAppObject(GUIObject):
    '''gui_options - None'''
    BUTTON_PATHS = [f'resources/gfx/kahoot/kahoot-{color}.png' for color in ('red', 'blue', 'green', 'yellow')]
    BUTTON_OPTIONS = [
        (RESOLUTION[0] // 4, RESOLUTION[1] // 4 * 3 - 40), (RESOLUTION[0] // 4 * 3, RESOLUTION[1] // 4 * 3 - 40),
        (RESOLUTION[0] // 4, RESOLUTION[1] // 4 * 3 + 100), (RESOLUTION[0] // 4 * 3, RESOLUTION[1] // 4 * 3 + 100),
    ]
    GONG_SOUND = pygame.mixer.Sound('resources/sfx/sounds/kahoot-gong.ogg')

    class Question:
        IMAGE_OPTIONS = (RESOLUTION[0] // 2, RESOLUTION[1] // 2 - 100)
        QUESTION_TEXT_OPTIONS = (RESOLUTION[0] // 2, 50)

        def __init__(self, question, answers, correct, image=None):
            self.question_text = TextObject(self.QUESTION_TEXT_OPTIONS, question, size=30, font='Helvetica', visible=False)
            self.answers = []
            for options, answer in zip(KahootAppObject.BUTTON_OPTIONS, answers):
                if len(answer) > 30:
                    options = (options[0], options[1] - 40)
                self.answers.append(TextObject(options, answer, color=Color.white, size=20, max_len=30, spacing=20, font='Helvetica'))
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
        self._app_instance.global_objects['timer'].disable()
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
                        self.return_back()
                        if not self._app_instance.current_level.get_object('elevator_button_up').enabled:
                            self._app_instance.global_objects['timer'].increase(minutes=2)
                            self.GONG_SOUND.play()
                    break
            self.clicked = False

    def update(self):
        # Last question is correct
        if self.current_question == len(self.questions):
            self.return_back()
            elevator_button = self._app_instance.current_level.get_object('elevator_button_up')
            if not elevator_button.enabled:
                self._app_instance.global_objects['timer'].decrease(minutes=15)
                elevator_button.enabled = True

    def draw(self, screen):
        if self.current_question == -1:
            return

        for button in self.buttons:
            button.draw(screen)
        self.questions[self.current_question].draw(screen)

    def return_back(self):
        self.current_question = -1
        self._app_instance.global_objects['timer'].enable()
        for gui_object in self._app_instance.current_level.get_all_objects():
            if gui_object.name != 'instructions_message':
                gui_object.enable()


class TaskPanelObject(GUIObject):
    '''gui_options - None'''
    PANEL_PATH = 'resources/gfx/task-panel/panel.png'
    TASK_POINTS = [5000, 1500, 1000, 800, 100]

    class Task:
        TIMEOUT = 10

        def __init__(self, task_name, task_text, time_limit, tests):
            self.name = task_name
            self.text = task_text
            self.time_limit = time_limit
            self.tests = tests

        def submit(self, parent):
            parent.submit_message.update_text('Automatic correction in progress... Please wait.', Color.inactive)
            result = self._process_submit()
            parent.result = result

            message_dict = {
                'OK': ('Success!', Color.success),
                'WA': ('Wrong answer!', Color.error),
                'TLE': ('Time limit exceeded.', Color.error),
                'EXC': ('Your program returned non zero value (see console).', Color.error),
                'FNF': (f'File {self.name + ".py"} not found in submits folder', Color.warning),
                'ERR': ('Something went seriously wrong. Check console and contact admin.', Color.error),
            }
            parent.submit_message.update_text(*message_dict[result])

        def _process_submit(self):
            start_time = time.time()
            for test_input, correct_output in self.tests:
                try:
                    for cmd in 'python', 'python3':
                        process = Popen([cmd, f'submits/{self.name}.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                        user_output, error_output = process.communicate(input=test_input, timeout=self.TIMEOUT)
                        if not process.returncode:
                            break
                        if process.returncode == 2:
                            return 'FNF'
                    else:
                        print(error_output)
                        return 'EXC'
                except TimeoutExpired:
                    process.kill()
                    return 'TLE'
                except Exception as exc:
                    print(exc)
                    return 'ERR'
                if user_output != correct_output + '\n':
                    return 'WA'
                if time.time() - start_time > self.time_limit:
                    return 'TLE'
            return 'OK'

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
        self.task_number_text = TextObject((x_mid - 50, y_mid - 205), '1', color=Color.red, size=40)
        self.timer_object = self._app_instance.global_objects['timer']
        self.time_text = TextObject((self.x + 180, self.y + 47), TimerObject.convert_time(self.timer_object.get_time()), centered=True, color=Color.red, size=25)
        self.current_task = 0
        self.is_completed = False
        self.result = None
        self.tasks = [self.Task(*task) for task in TASKS]
        self.submit_message = TextObject((x_mid, y_mid + 45), f'Leave {self.tasks[0].name + ".py"} in sumbits folder and press SUBMIT to submit.',
                                         color=Color.warning, max_len=28, spacing=15, centered=True)
        self.messages = [MessageObject((200, 200, 800), task.text, obj_id=self.obj_id, app=self._app_instance) for task in self.tasks]
        self.solving_time_start = time.time()
        self.final_points = 0

    def handle_event(self, event):
        if self.messages[self.current_task].reactive:
            self.messages[self.current_task].handle_event(event)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.elevator_button.reactive and self.elevator_button.collision():
                self.final_points = int(max(0, 20 * 60 - time.time() + self.solving_time_start) * 3) + self.TASK_POINTS[self.current_task]
                self.elevator_button.disable()
                self._app_instance.current_level.get_object('elevator_button_down').enable()
            if self.is_completed:
                return
            if self.button_submit.collision():
                thread = threading.Thread(target=self.tasks[self.current_task].submit, args=[self])
                thread.start()
            elif self.button_task.collision():
                self.messages[self.current_task].enable()
            elif self.left_arrow.reactive and self.left_arrow.collision():
                self.current_task -= 1
                self.submit_message.update_text(f'Leave {self.tasks[self.current_task].name + ".py"} in sumbits folder and press SUBMIT to submit.')
                self.task_number_text.update_text(str(self.current_task + 1))
            elif self.right_arrow.reactive and self.right_arrow.collision():
                self.current_task += 1
                self.submit_message.update_text(f'Leave {self.tasks[self.current_task].name + ".py"} in sumbits folder and press SUBMIT to submit.')
                self.task_number_text.update_text(str(self.current_task + 1))

    def update(self):
        if self.result == 'OK':
            self.is_completed = True
            self.panel_top.disable()
            self.elevator_button.enable()
            self.task_number_text.update_text(color=Color.success)
            self.time_text.update_text(color=Color.green)
            self.timer_object.stop()
            self.timer_object.disable()
            self.timer_object.dead = True
            self.result = None

        if self.messages[self.current_task].active:
            self.messages[self.current_task].update()

        if self.current_task != 0:
            self.left_arrow.enable()
        else:
            self.left_arrow.disable()
        if self.current_task != self.timer_object.stage - 1:
            self.right_arrow.enable()
        else:
            self.right_arrow.disable()
        
        if self.time_text.text != self.timer_object.time_text.text:
            self.time_text.update_text(self.timer_object.time_text.text)
        
        if self.current_task + 1 > self.timer_object.stage:
            self.current_task -= 1
            self.task_number_text.update_text(text=str(self.current_task + 1))

    def draw(self, screen):
        self.panel.draw(screen)
        
        self.task_number_text.draw(screen)
        self.time_text.draw(screen)
        self.button_submit.draw(screen)
        self.button_task.draw(screen)
        self.submit_message.draw(screen)

        if self.left_arrow.visible:
            self.left_arrow.draw(screen)
        if self.right_arrow.visible:
            self.right_arrow.draw(screen)
        if self.elevator_button.visible:
            self.elevator_button.draw(screen)
        if self.panel_top.visible:
            self.panel_top.draw(screen)

        if self.messages[self.current_task].visible:
            self.messages[self.current_task].draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.panel.move_coords(x, y)
        self.messages[self.current_task].move_coords(x, y)
        self.button_task.move_coords(x, y)
        self.button_submit.move_coords(x, y)
        self.elevator_button.move_coords(x, y)
        self.panel_top.move_coords(x, y)
        self.left_arrow.move_coords(x, y)
        self.right_arrow.move_coords(x, y)
        self.submit_message.move_coords(x, y)
        self.task_number_text.move_coords(x, y)
        self.time_text.move_coords(x, y)


class SwitchObject(GUIObject):
    '''gui_options - (x, y, width, height)'''
    PANEL_IMAGE_PATH = 'resources/gfx/switch/switch-panel.png'
    SWITCH_BUTTON_IMAGE_PATH = 'resources/gfx/switch/switch-button.png'

    def __init__(self, gui_options, switch_function, status=False, **kwargs):
        super().__init__(*gui_options, **kwargs)
        self.panel_img = ImageObject((self.x, self.y), self.PANEL_IMAGE_PATH, scale=(self.width, self.height))
        self.switch_button = ImageObject((self.x + self.width // 4, self.y + self.height // 2),
                                          self.SWITCH_BUTTON_IMAGE_PATH, scale=(self.width // 2 - 5, self.height - 5), centered=True)
        self.switch_function = switch_function
        self.clicked = False
        self.status = status

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.switch_button.collision():
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.switch_button.collision() and self.clicked and self.visible:
                self.status = not self.status
                self.switch_function(self._app_instance, self.status)
                MoveObjectAnimation(self.switch_button, self.x + self.width // 2 * self.status, self.y, app=self._app_instance)
            self.clicked = False

    def draw(self, screen):
        self.panel_img.draw(screen)
        self.switch_button.draw(screen)

    def move_coords(self, x, y):
        super().move_coords(x, y)
        self.panel_img.move_coords(x, y)
        self.switch_button.move_coords(x, y)


class TimerObject(GUIObject):
    '''gui_options - (x, y, width, height)'''
    TIMER_PANEL_IMG_PATH = 'resources/gfx/timer/timer-panel.png'

    def __init__(self, gui_options, **kwargs):
        super().__init__(*gui_options, active=False, **kwargs)
        self.stage = 1
        self._seconds = 60 * 20  # 20:00
        self.panel_img = ImageObject(gui_options, self.TIMER_PANEL_IMG_PATH, scale=(self.width, self.height), centered=True)
        self.time_text = TextObject((self.x + 20, self.y), TimerObject.convert_time(self._seconds), centered=True, color=Color.red, size=25)
        self.stage_text = TextObject((self.x - self.width // 3, self.y), str(self.stage), centered=True, color=Color.red, size=30)
        self.time_change_text = None
        self.time = time.time()
        self.dead = False

    def update(self):
        if time.time() - self.time > 1:
            self.decrease(seconds=1, animation=False)
            self.time += 1
            self.time_text.update_text(TimerObject.convert_time(self._seconds))

        if self._seconds > 20 * 60:
            if self.stage > 1:
                self.stage -= 1
                self._seconds %= 20 * 60
            else:
                self._seconds = 20 * 60
            self.time_text.update_text(TimerObject.convert_time(self._seconds))
            self.stage_text.update_text(str(self.stage))
        elif self._seconds <= 0:
            if self.stage < 5:
                self.stage += 1
                self._seconds = 20 * 60 + self._seconds
            else:
                self._seconds = 0
            self.time_text.update_text(TimerObject.convert_time(self._seconds))
            self.stage_text.update_text(str(self.stage))


    def draw(self, screen):
        self.panel_img.draw(screen)
        self.time_text.draw(screen)
        self.stage_text.draw(screen)
        if self.time_change_text is not None:
            self.time_change_text.draw(screen)

    def get_time(self):
        return self._seconds

    @staticmethod
    def convert_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f'{minutes:02}:{seconds:02}'

    def start(self):
        self.time = time.time()
        self.active = True
    
    def stop(self):
        self.active = False

    def increase(self, minutes=0, seconds=0, animation=True):
        if self.dead:
            return
        self._seconds += seconds + minutes * 60
        if animation:
            self._animate_timer_change(seconds + minutes * 60)

    def decrease(self, minutes=0, seconds=0, animation=True):
        self.increase(minutes=-minutes, seconds=-seconds, animation=animation)

    def enable(self):
        if not self.dead:
            super().enable()

    def _animate_timer_change(self, seconds):
        color = Color.green if seconds < 0 else Color.red
        sign = '-' if seconds < 0 else '+'
        self.time_change_text = TextObject((self.x + self.width // 2, self.y), f'{sign}{TimerObject.convert_time(abs(seconds))}', color=color, centered=True, size=25)
        MoveObjectAnimation(self.time_change_text, self.time_change_text.x, self.time_change_text.y - 30, disappear=True, app=self._app_instance)


class ChangeLevelObject(GUIObject):
    '''gui_options - (x, y)'''
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
    'message': MessageObject,
    'image': ImageObject,
    'input': InputObject,
    'kahoot': KahootAppObject,
    'level_changer': ChangeLevelObject,
    'switch': SwitchObject,
    'task_panel': TaskPanelObject,
    'text': TextObject,
    'timer': TimerObject,
}
