# Final floor


def show_instructions_click(app):
    app.current_level.get_object('final_instructions').enable()


BACKGROUND = 'resources/gfx/backgrounds/bg-hacking.png'
MUSIC = 'resources/sfx/themes/final-theme.mp3'

OBJECTS = {
    'hidden_panel': {
        'type': 'image',
        'options': {
            'gui_options': (640, 360),
            'image_path': 'resources/gfx/elevator/elevator-panel.png',
            'scale': (100, 200),
            'reactive': False,
            'centered': True,
        }
    },

    'hidden_button_1': {
        'type': 'image',
        'options': {
            'gui_options': (530, 430),
            'image_path': 'resources/gfx/elevator/elevator-down.png',
            'scale': (50, 50),
            'reactive': False,
            'centered': True,
        }
    },

    'hidden_button_2': {
        'type': 'image',
        'options': {
            'gui_options': (750, 430),
            'image_path': 'resources/gfx/elevator/elevator-down.png',
            'scale': (50, 50),
            'reactive': False,
            'centered': True,
        }
    },

    'final_input': {
        'type': 'input',
        'options': {
            'gui_options': (530, 530, 220, 50),
            'task': '',
            'answer': 'napolitanka1',
            'correct': '',
            'wrong': '',
        }
    },

    'silence_button': {
        'type': 'button',
        'options': {
            'gui_options': (540, 600, 200, 70),
            'on_click': show_instructions_click,
            'content': {
                'type': 'text',
                'options': {
                    'text': 'Oh no!',
                    'font': 'Times New Roman',
                    'size': 30,
                    'color': (255, 255, 255),
                }
            }
        }
    },

    'lock_image': {
        'type': 'image',
        'options': {
            'gui_options': (640, 250),
            'image_path': 'resources/gfx/misc/lock.png',
            'scale': (400, 500),
            'centered': True,
        }
    },

    'final_instructions': {
        'type': 'message',
        'options': {
            'gui_options': (300, 200, 600),
            'text': 'There is a crack tutorial, but too complicated... https://uloz.to/file/cSiNGwFwpjfP/crack-zip',
        }
    },

    'elevator_panel': {
        'type': 'image',
        'options': {
            'gui_options': (1050, 150),
            'image_path': 'resources/gfx/elevator/elevator-panel.png',
            'visible': False,
        }
    },

    'elevator_button_down': {
        'type': 'level_changer',
        'options': {
            'gui_options': (1100, 350),
            'direction': 'down',
            'visible': False,
            'active': False,
            'reactive': False,
        }
    },
}
