# Submit floor

BACKGROUND = 'resources/gfx/backgrounds/bg-brick-wall.png'
MUSIC = 'resources/sfx/themes/submit-room-music.mp3'

OBJECTS = {
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

    'welcome_message': {
        'type': 'message',
        'options': {
            'gui_options': (300, 200, 600),
            'text': 'Vitaj. Toto je testovač. Testovač treba poraziť. Akonáhle je testovač porazený, nebude sa dať poraziť znovu. Čím skôr porazíš testovač, tým viac ťa odmení. Mimochodom, príde ti "$" ako zaujímavý argument?',
            'enabled': True,
        }
    }
}
