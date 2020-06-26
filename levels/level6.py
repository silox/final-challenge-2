# Silent floor

def silence_button_click(app, only_once_checker=[True]):
    app.current_level.get_object('silence_message').enable()
    if only_once_checker[0]:
        app.global_objects['timer'].decrease(minutes=10)
        only_once_checker[0] = False


BACKGROUND = 'resources/gfx/backgrounds/bg-silence.png'
MUSIC = 'resources/sfx/themes/calm.mp3'

OBJECTS = {
    'calm_text': {
        'type': 'image',
        'options': {
            'gui_options': (300, 200),
            'image_path': 'resources/gfx/misc/calm-text.png',
        }
    },

    'calm_text_light': {
        'type': 'image',
        'options': {
            'gui_options': (300, 200),
            'image_path': 'resources/gfx/misc/calm-text-light.png',
            'visible': False,
        }
    },

    'silence_button': {
        'type': 'button',
        'options': {
            'gui_options': (500, 600, 200, 70),
            'on_click': silence_button_click,
            'visible': False,
            'active': False,
            'reactive': False,
            'content': {
                'type': 'text',
                'options': {
                    'text': 'I feel relaxed',
                    'font': 'Times New Roman',
                    'size': 30,
                }
            }
        }
    },

    'silence_message': {
        'type': 'message',
        'options': {
            'gui_options': (300, 200, 500),
            'text': 'Ok then.',
        }
    },

    'elevator_panel': {
        'type': 'image',
        'options': {
            'gui_options': (1050, 150),
            'image_path': 'resources/gfx/elevator/elevator-panel.png',
        }
    },

    'elevator_button_up': {
        'type': 'level_changer',
        'options': {
            'gui_options': (1100, 200),
            'direction': 'up',
        }
    },

    'elevator_button_down': {
        'type': 'level_changer',
        'options': {
            'gui_options': (1100, 350),
            'direction': 'down',
        }
    },
}
