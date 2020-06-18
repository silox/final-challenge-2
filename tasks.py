from random import randrange


TASKS = [
    (
        'binary_search',
        'Vstup obsahuje 2 riadky. Na prvom riadku je n (n >= 1) unikátnych celých čísel oddelených medzerami, usporiadaných vzostupne. '
        'Na druhom riadku k (k >= 1) celých čísel. Pre každé číslo k zisti, či sa vyskytuje v prvom riadku. '
        'Ak áno, vypíš jeho index, inak -1. Každý index vypisuj na nový riadok',
        5,  # Time limit in seconds
        [
            ('-1\n-1', '0'),
            ('0 2\n0', '0'),
            ('0 2\n2', '1'),
            ('0 2\n1', '-1'),
            ('0 2\n-1', '-1'),
            ('0 2\n10', '-1'),
            ('0 2 5\n0 4', '0\n-1'),
            ('0 2 5\n2', '1'),
            ('0 2 5\n5', '2'),
            ('0 2 5\n18', '-1'),
            ('-3 18 25 26 27 28\n26 25 -3 28 0', '3\n2\n0\n5\n-1'),
            (' '.join(map(str, range(100000))) + '\n' + ' '.join(map(str, range(100000))), '\n'.join(map(str, range(100000)))),
        ],
    ),
    (
        '', '', 3, []
    ),
    (
        'int_sum',
        'Na vstupe je n (n >= 1) medzerou oddelených čísel. Vypíš ich súčet.',
        2,  # Time limit in seconds
        [
            ('-1000', '-1000'),
            ('1 2 3', '6'),
            ('-1 -1 3', '1'),
            ('0 0 0 0 0 0 0 0 0 0', '0'),
            ('112 150 155 158 159', '734'),
            ('22 23', '45'),
        ]
    ),
]
