# Kahoot level

MUSIC = 'resources/sfx/themes/kahoot-music.mp3'


def start_click(app):
    for gui_object in app.current_level.get_all_objects():
        gui_object.disable()
    app.current_level.get_object('kahoot').start()


def instructions_click(app):
    app.current_level.get_object('instructions_dialogue').enable()


kahoot_questions_data = [
    {
        'question': 'Ktorá odpoveď je správna?',
        'answers': ('Správna odpoveď je modrá', 'Červená odpoveď klame', 'Žltá odpoveď klame', 'Modrá odpoveď hovorí pravdu'),
        'correct': 1,
        'image': 'resources/gfx/kahoot/kahoot-image1.png',
    },
    {
        'question': 'Ktorý z týchto programovacích jazykov dokáže preložiť kód, pretože neobsahuje syntaktickú chybu?',
        'answers': ('C', 'Pascal', 'Python', 'C++'),
        'correct': 2,
        'image': 'resources/gfx/kahoot/kahoot-image2.png',
    },
    {
        'question': 'Aká je časová zložitosť algoritmu na obrázku, ak si označíme n ako dĺžku array?',
        'answers': ('O(log(n)) - logaritmická', 'O(n) - lineárna', 'O(n * log(n))', 'O(n^2) - kvadratická'),
        'correct': 3,
        'image': 'resources/gfx/kahoot/kahoot-image3.png',
    },
    {
        'question': 'Aké je najvhodnejšie pomenovanie grafu na obrázku?',
        'answers': ('Acyklický neorientovaný', 'Cyklický neorientovaný', 'Acyklický orientovaný', 'Cyklický orientovaný'),
        'correct': 2,
        'image': 'resources/gfx/kahoot/kahoot-image4.png',
    },
    {
        'question': 'Koľko komponent má graf na obrázku?',
        'answers': ('1', '2', '7', '8'),
        'correct': 1,
        'image': 'resources/gfx/kahoot/kahoot-image5.png',
    },
    {
        'question': 'Je na obrázku korektný binárny strom?',
        'answers': ('Áno', 'Nie', 'To bude isto habaďúra', 'Táto možnosť tu vôbec nie je preto, že sa mi nechcelo implementovať menej ako 4 možné odpovede'),
        'correct': 0,
        'image': 'resources/gfx/kahoot/kahoot-image6.png',
    },
    # {
    #     'question': '',
    #     'answers': ('', '', '', ''),
    #     'correct': ,
    #     'image': 'resources/gfx/kahoot/kahoot-image.png',
    # },
    # {
    #     'question': '',
    #     'answers': ('', '', '', ''),
    #     'correct': ,
    #     'image': 'resources/gfx/kahoot/kahoot-image.png',
    # },
]

OBJECTS = {
    'kahoot': {
        'type': 'kahoot',
        'options': {
            'questions': kahoot_questions_data,
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
