# Easy input box level

def tiny_button_click(app):
    music_title = app.current_level.get_object('music_title')
    if not music_title.visible:
        app.global_objects['timer'].decrease(minutes=5)
    music_title.enable()


BACKGROUND = 'resources/gfx/backgrounds/bg-meadow.png'
MUSIC = 'resources/sfx/themes/wii-music.mp3'

OBJECTS = {
    'input_1': {
        'type': 'input',
        'options': {
            'gui_options': (150, 150, 210, 32),
            'task': '1 + 1 = ?',
            'answer': '2',
            'correct': 'Si geniálny!',
            'wrong': 'Hádam si si nemyslel, že 10...',
            'sfx': True,
            'reward': 60,
        }
    },

    'input_2': {
        'type': 'input',
        'options': {
            'gui_options': (700, 150, 210, 32),
            'task': 'Aké je tretie písmeno anglickej abecedy?',
            'answer': 'c',
            'correct': 'Presne tak, si úžasný!',
            'wrong': 'Hint: Je to písmeno medzi "b" a "d"',
            'sfx': True,
            'reward': 60,
        }
    },

    'input_3': {
        'type': 'input',
        'options': {
            'gui_options': (150, 550, 210, 32),
            'task': 'Ako sa píše slovo "paradajka"?',
            'answer': 'paradajka',
            'correct': 'Áno, to je ono!',
            'wrong': 'Nevadí, nie každý to zvládne na prvý krát.',
            'sfx': True,
            'reward': 60,
        }
    },

    'input_4': {
        'type': 'input',
        'options': {
            'gui_options': (700, 550, 210, 32),
            'task': 'Ako sa povie po Anglicky mačka?',
            'answer': 'cat',
            'correct': 'This one was trickier, but you got it. You truly are a hero!',
            'wrong': 'Má to iba 3 písmená. Pri najhoršom to dáš na 17576. pokus :)',
            'sfx': True,
            'reward': 120,
        }
    },

    'tiny_button': {
        'type': 'button',
        'options': {
            'gui_options': (365, 330, 10, 10),
            'outline': (234, 246, 255),
            'on_click': tiny_button_click,
        }
    },

    'music_title': {
        'type': 'text',
        'options': {
            'gui_options': (850, 350),
            'text': 'Song name: Mii chanel theme',
            'size': 20,
            'font': 'Helvetica',
            'visible': False,
        }
    },

    'kanna_point_image': {
        'type': 'image',
        'options': {
            'gui_options': (540, 350),
            'image_path': 'resources/gfx/misc/kanna-point.png',
            'centered': True,
            'scale': (350, 300),
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
