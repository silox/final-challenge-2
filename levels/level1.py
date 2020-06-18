BACKGROUND = 'resources/gfx/adverts/ad3.png'
# MUSIC = 'resources/sfx/themes/ruski-melody.mp3'

OBJECTS = {
    'sample_input': {
        'type': 'input',
        'options': {
            'gui_options': (100, 50, 210, 32),
            'task': '1 + 1 = ?',
            'answer': '10',
            'correct': 'Wow, si geniálny!',
            'wrong': 'je mi ľúto, ale 2 to nie je :D',
            'sfx': True,
        }
    },

    'task_panel': {
        'type': 'task_panel',
        'options': {}
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
            'enabled': True,
            'reactive': False,
            'active': False,
            'visible': False,
        }
    },
}
