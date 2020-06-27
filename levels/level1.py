# Basement floor


def switch_mode(app, status):
    app.easy_mode = status


BACKGROUND = 'resources/gfx/backgrounds/bg-dark-room.png'
MUSIC = 'resources/sfx/themes/basement.mp3'

OBJECTS = {
    'switch': {
        'type': 'switch',
        'options': {
            'gui_options': (550, 300, 200, 100),
            'switch_function': switch_mode,
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
            'enabled': True,
        }
    },

    'elevator_button_down': {
        'type': 'level_changer',
        'options': {
            'gui_options': (1100, 350),
            'direction': 'down',
            'reactive': False,
            'active': False,
            'visible': False,
        }
    },
}
