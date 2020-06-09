BACKGROUND = 'resources/gfx/elevator-up-light.png'
MUSIC = 'resources/sfx/megalovania.mp3'

OBJECTS = {
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
