# Kahoot level

# MUSIC = 'resources/sfx/themes/kahoot-music.mp3'


def start_click(app):
    for gui_object in app.current_level.get_all_objects():
        gui_object.hide()
    kahoot_app = app.current_level.get_object('kahoot').start()


def instructions_click(app):
    app.current_level.get_object('instructions_dialogue').show()


OBJECTS = {
    'kahoot': {
        'type': 'kahoot',
        'options': {
            'questions_data': [
                {
                    'question': 'Sample question',
                    'answers': ('this is incorrect', 'but this is right', 'gg', 'wp'),
                    'correct': 1,
                    'image': None,
                },
                {
                    'question': 'Another question',
                    'answers': ('last one will be right', 'hello', 'trying some longer textooooooooooooooooooooo omg omg omg omg omg omg', 'hi is right?!'),
                    'correct': 3,
                },
            ],
        }
    },

    'kahoot_logo': {
        'type': 'image',
        'options': {
            'gui_options': (400, 100),
            'image_path': 'resources/gfx/kahoot/kahoot-logo.png',
            'scale': (500, 200),
        }
    },

    'start_button': {
        'type': 'button',
        'options': {
            'gui_options': (500, 400, 200, 70),
            'on_click': start_click,
            'outline': (255, 0, 0),
            'content': {
                'type': 'text',
                'options': {
                    'text': 'Start',
                    'font': 'Times New Roman',
                    'size': 30,
                }
            }
        }
    },

    'instructions_button': {
        'type': 'button',
        'options': {
            'gui_options': (500, 500, 200, 70),
            'on_click': instructions_click,
            'content': {
                'type': 'text',
                'options': {
                    'text': 'Instructions',
                    'font': 'Times New Roman',
                    'size': 30,
                }
            }
        }
    },

    'instructions_dialogue': {
        'type': 'dialogue',
        'options': {
            'gui_options': (300, 200, 550, 200),
            'text': 'Kahoot not a lie? Yes, Kahoot lie. Kahoot bad. Hotkao the best! Hotkao trestá za nesprávnu odpoveď. Nenechaj sa potrestať!'
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
            'enabled': True,
        }
    },
}
