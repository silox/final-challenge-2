BACKGROUND = 'resources/gfx/ad3.png'
MUSIC = 'resources/sfx/ruski-melody.mp3'

OBJECTS = {
    'sample_input_box': {
        'type': 'input_box',
        'options': {
            'gui_options': (100, 50, 210, 32),
            'task': '1 + 1 = ?',
            'answer': '10',
            'correct': 'Wow, si geniálny!',
            'wrong': 'je mi ľúto, ale 2 to nie je :D',
            'sfx': True,
        }
    },

    'sample_dialogue': {
        'type': 'dialogue_box',
        'options': {
            'gui_options': (300, 200, 400, 300),
            'text': 'Sample text',
        }
    },

    'sample_advert': {
        'type': 'advert',
        'options': {
            'gui_options': (100, 100, 0, 0),
            'image_path': 'resources/gfx/but-close.png',
            'url': 'google.com',
        }
    },

    'elevator_panel': {
        'type': 'image',
        'options': {
            'gui_options': (1050, 150, 0, 0),
            'image_path': 'resources/gfx/elevator-panel.png',
        }
    },

    'elevator_button_up': {
        'type': 'level_changer',
        'options': {
            'gui_options': (1100, 200, 0, 0),
            'direction': 'up',
            'enabled': True,
        }
    },

    'elevator_button_down': {
        'type': 'level_changer',
        'options': {
            'gui_options': (1100, 350, 0, 0),
            'direction': 'down',
            'enabled': True,
        }
    },
}
