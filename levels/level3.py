OBJECTS = {
    'sample_input_box': {
        'type': 'input',
        'options': {
            'gui_options': (300, 110, 150, 100),
            'task': '1 + 1 = ?',
            'answer': '10',
            'correct': 'Wow, si geniálny!',
            'wrong': 'je mi ľúto, ale 2 to nie je :D',
            'sfx': True,
        }
    },

    'sample_advert': {
        'type': 'advert',
        'options': {
            'gui_options': (100, 100),
            'image_path': 'resources/gfx/adverts/ad1.png',
            'url': 'google.com',
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
            'enabled': True,
        }
    },
}
