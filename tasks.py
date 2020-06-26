TASKS = [
    (
        'graph_dist',
        'Na prvom riadku vstupu 2 medzerou oddelené čísla N (počet vrcholov) a M (počet hrán), kde platí N >= 1, 0 <= M < N. '
        'Na druhom riadku sú 3 medzerou oddelené čísla, A, B, K, ktoré predstavujú konkrétne vrcholy. Ďalej nasleduje M riadkov '
        'dvojíc čísel, ktoré značia, že je medzi danými vrcholmi hrana. Vstup teda predstavuje neorientovaný, neohodnotený graf, '
        'ktorý obsahuje vrcholy očíslované od 0 po N - 1. Na výstup vypíš jedno číslo a to najkratšiu vzdialenosť z vrcholu A do '
        'vrcholu B tak, aby cesta prechádzala cez vrchol K. Platí 0 <= A, B, K < N. Graf neobsahuje sľučky.',
        2,  # Time limit in seconds
        [
            ('1 0\n0 0 0', '0'),
            ('2 0\n0 0 1', '-1'),
            ('5 1\n4 4 4\n2 1', '0'),
            ('5 4\n1 3 2\n1 0\n1 2\n1 3\n1 4', '3'),
            ('5 4\n3 2 1\n1 0\n1 2\n1 3\n1 4', '2'),
            ('6 6\n2 5 0\n0 1\n1 2\n2 3\n3 4\n4 5\n5 0\n', '3'),
            ('7 6\n0 6 1\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n', '6'),
            ('7 6\n4 6 0\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n', '10'),
            ('6 8\n0 5 4\n0 1\n0 2\n2 1\n2 5\n5 4\n4 3\n3 5\n3 5', '4'),
        ],
    ),

    (
        'prefix_sum',
        'V prvom riadku sa nachádzajú celé čísla oddelené medzerou. V druhom riadku je celé číslo N (N > 0). Nasleduje N riadkov. '
        'Každý z nich obsahuje 2 medzerou oddelené celé čísla a[i], b[i], ktoré predstavujú indexy pola z prvého riadku. Pre každú '
        'dvojicu čísel a, b vypíš súčet čísel v poli od indexu a po index b vrátane. Pre každé i platí, a[i] <= b[i].',
        8,  # Time limit in seconds
        [
            ('-1\n2\n0 0\n0 0', '-1\n-1'),
            ('1 2\n1\n0 1', '3'),
            ('8 0 -32 45 33 22\n5\n0 0\n1 3\n4 4\n0 5\n4 5', '8\n13\n33\n76\n55'),
            ('5 4 2 1 0 0 0\n2\n6 6\n2 5', '0\n3'),
            # speed test
            (' '.join(map(str, range(100000))) + '\n100000' + '\n101 89998' * 100000, '\n'.join('4049859951' for _ in range(100000))),
        ]
    ),

    (
        'bracket_madness',
        'Na jednom riadku vstupu sa nachádza neprázdny reťazec pozostávajúci zo znakov "([)]". Pokiaľ tento reťazec reprezentuje '
        'korektne uzátvorkovaný výraz, vypíš "hotkao", inak "kahoot" (bez úvodzoviek). Príklady korektne uzátvorkovaných výrazov: '
        '"[]", "([()])()", "[]()()()[]". Zle uzátvorkované výrazy: "[[", "([)]", ")()(".',
        3,  # time limit in seconds
        [
            ('()', 'hotkao'),
            ('()())(', 'kahoot'),
            ('[(])', 'kahoot'),
            ('((((())))[])[[]]()[][](([[]()]))', 'hotkao'),
            ('((((())))[])[[]]()[][](([[]()]))]', 'kahoot'),
            ('[((((())))[])[[]]()[][](([[]()]))', 'kahoot'),
            ('[][][]', 'hotkao'),
            ('(())[[]]', 'hotkao'),
            (')', 'kahoot'),
            ('[', 'kahoot'),
        ]
    ),

    (
        'binary_search',
        'Vstup obsahuje 2 riadky. Na prvom riadku je n (n >= 1) unikátnych celých čísel oddelených medzerami, usporiadaných vzostupne. '
        'Na druhom riadku k (k >= 1) celých čísel. Pre každé číslo k zisti, či sa vyskytuje v prvom riadku. '
        'Ak áno, vypíš jeho index, inak -1. Každý index vypisuj na nový riadok',
        8,  # Time limit in seconds
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
            # speed test
            (' '.join(map(str, range(100000))) + '\n' + ' '.join(map(str, range(100000))), '\n'.join(map(str, range(100000)))),
        ],
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
