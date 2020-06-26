# Advert floor

BACKGROUND = 'resources/gfx/backgrounds/bg-adverts.png'
MUSIC = 'resources/sfx/themes/advert-music.mp3'

OBJECTS = {
    'input_1': {
        'type': 'input',
        'options': {
            'gui_options': (150, 150, 210, 32),
            'task': '2020. prvočíslo v poradí?',
            'answer': '17573',
            'correct': 'Milujem hľadanie prvočísel pri pozeraní reklám!',
            'wrong': 'Ten rok je snáď prekliaty!',
            'reward': 2 * 60,
            'sfx': True,
        }
    },

    'input_2': {
        'type': 'input',
        'options': {
            'gui_options': (700, 150, 210, 32),
            'task': 'caesar <- Wrwr mh vsudyqd rgsryhg',
            'answer': 'zxbpxo',
            'correct': 'Nemám čas počúvať iba jednu hudbu naráz.',
            'wrong': 'Kocky som stratil',
            'reward': 3 * 60,
            'sfx': True,
        }
    },

    'input_3': {
        'type': 'input',
        'options': {
            'gui_options': (150, 520, 210, 32),
            'task': 'Šieste slovo v popisku 2. najsledovanejšieho videa na YT?',
            'answer': 'pinkfong',
            'correct': 'To určite nie je správne video :D',
            'wrong': 'Cítim z teba ten cringe feeling',
            'reward': 4 * 60,
            'sfx': True,
        }
    },

    'input_4': {
        'type': 'input',
        'options': {
            'gui_options': (700, 520, 210, 32),
            'task': '',
            'answer': 'kamzik',
            'synonyms': ('chamois',),
            'correct': 'To ti muselo zabrať veľa času',
            'wrong': 'Kľud, máš čas.',
            'reward': 5 * 60,
            'sfx': True,
        }
    },

    'task_4_image': {
        'type': 'image',
        'options': {
            'gui_options': (640, 450),
            'image_path': 'resources/gfx/misc/japanese-translate.png',
            'scale': (350, 60),
        }
    },

    'ad_1': {
        'type': 'advert',
        'options': {
            'gui_options': (50, 50),
            'image_path': 'resources/gfx/adverts/ad-granny.png',
            'url': 'https://badoo.com/',
        }
    },

    'ad_2': {
        'type': 'advert',
        'options': {
            'gui_options': (600, 50),
            'image_path': 'resources/gfx/adverts/ad-iphone.png',
            'url': 'https://ih1.redbubble.net/image.1027498235.4407/flat,750x,075,f-pad,750x1000,f8f8f8.jpg',
        }
    },

    'ad_3': {
        'type': 'advert',
        'options': {
            'gui_options': (50, 400),
            'image_path': 'resources/gfx/adverts/ad-tanki.png',
            'url': 'https://tankionline.com/play/',
        }
    },

    'ad_4': {
        'type': 'advert',
        'options': {
            'gui_options': (600, 400),
            'image_path': 'resources/gfx/adverts/ad-ram.png',
            'url': 'https://www.youtube.com/watch?v=4XuUyfywhGQ',
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
