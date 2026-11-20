"""ONE TICKET OUT - three kids race; the winner saves one family."""
from shorts.scene import (HALF, OFF, close_up, cover, face, hold, kf, medium,
                          shot, split_shots, wide)  # noqa: F401

TITLE = "ONE TICKET OUT"

BEATS = [
    {"id": "b1", "text": "In this town, three kids race for one ticket out. The winner saves one family.", "pause": 0.08},
    {"id": "b2", "text": "The other two are sent away. This year, I was one.", "pause": 0.06},
    {"id": "b3", "text": "I had to win. Mom was sick, and the city had the only doctor.", "pause": 0.08},
    {"id": "b4", "text": "June was my best friend. Dex had never won.", "pause": 0.06},
    {"id": "b5", "text": "The whole school came to watch.", "pause": 0.06},
    {"id": "b6", "text": "The gate opened. We ran.", "pause": 0.06},
    {"id": "b7", "text": "I was faster than both of them... until June's leg gave out.", "pause": 0.06},
    {"id": "b8", "text": "The rules said keep running. I turned back.", "pause": 0.10},
    {"id": "b9", "text": "I matched her pace. Dex passed us both.", "pause": 0.08},
    {"id": "b10", "text": "He screamed: you lost your mom's only chance!", "pause": 0.06},
    {"id": "b11", "text": "But at the gate, Dex stopped.", "pause": 0.12},
    {"id": "b12", "text": "Years ago, he stopped for a friend and lost everything.", "pause": 0.14},
    {"id": "b13", "text": "Now I had the choice he never got.", "pause": 0.12},
    {"id": "b14", "text": "June slowed down... and waved me ahead.", "pause": 0.10},
    {"id": "b15", "text": "I could have stopped. I didn't.", "pause": 0.12},
    {"id": "b16", "text": "I won. I chose my mom. She got treatment.", "pause": 0.10},
    {"id": "b17", "text": "That night, June's family was sent away. She looked back once.", "pause": 0.10},
    {"id": "b18", "text": "She said she'd do the same. I still don't know if that's true.", "pause": 0.16},
    {"id": "b19", "text": "Who would you have saved: your mom... or your best friend?", "pause": 0.30},
]

MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b12+0.2", "b13.end"), ("b18.end-0.3", "b19.end+0.5")],
}

SFX = [
    ("b1", "whoosh"),
    ("b2+0.4", "pop", {"f": 560}),
    ("b3", "bell_low"),
    ("b4+0.3", "pop", {"f": 440}),
    ("b5", "swish"),
    ("b6", "whoosh"),
    ("b6+0.8", "riser", {"dur": 2.0}),
    ("b7.end-0.5", "thud"),
    ("b8", "bell_low"),
    ("b9+0.5", "swish"),
    ("b10", "impact"),
    ("b11", "ding_dong"),
    ("b12", "sad"),
    ("b13+0.6", "bell_low"),
    ("b14", "sparkle"),
    ("b15", "riser", {"dur": 1.4}),
    ("b16", "reveal"),
    ("b17", "whoosh"),
    ("b17+1.2", "sad"),
    ("b18", "bell_low"),
    ("b19", "twist"),
]

JUNE = {
    "extends": "kid_girl",
    "skin": "fair",
    "hair": {"style": "pigtails", "color": "auburn"},
    "top": {"style": "sweater", "color": "mustard", "secondary": "cream"},
    "bottom": {"style": "skirt", "color": "denim", "legs": "cream"},
    "shoes": {"style": "sneakers", "color": "white", "sole": "white"},
}

CAST = {
    "maya": {
        "extends": "kid_girl",
        "skin": "brown",
        "hair": {"style": "ponytail", "color": "black"},
        "top": {"style": "jacket", "color": "teal", "secondary": "white"},
        "bottom": {"style": "jeans", "color": "denim"},
        "shoes": {"style": "sneakers", "color": "white", "sole": "white"},
    },
    "june": JUNE,
    "june_night": JUNE,
    "dex": {
        "extends": "schoolboy",
        "skin": "tan",
        "hair": {"style": "buzz", "color": "black"},
        "top": {"style": "jacket", "color": "red", "secondary": "black"},
        "bottom": {"style": "pants", "color": "charcoal"},
        "shoes": {"style": "boots", "color": "black"},
    },
    "host": {"extends": "principal"},
    "mom": {
        "extends": "real_mom",
        "hair": {"style": "bun", "color": "black"},
        "top": {"style": "sweater", "color": "lavender", "secondary": "cream"},
        "bottom": {"style": "pants", "color": "charcoal"},
    },
    "crowd_a": {
        "extends": "schoolgirl",
        "skin": "light",
        "hair": {"style": "bob", "color": "blonde"},
        "top": {"style": "tshirt", "color": "sky", "secondary": "white"},
    },
    "crowd_b": {
        "extends": "schoolboy",
        "skin": "brown",
        "hair": {"style": "spikyAnime", "color": "brown"},
        "top": {"style": "hoodie", "color": "orange", "secondary": "white"},
    },
}


def scenes(T):
    B, E, END = T.B, T.E, T.END

    MAYA = [-4.8, 0, -3.5]
    JUNE_P = [4.8, 0, -3.5]
    DEX = [0, 0, -7.0]
    HOST = [6.6, 0, 1.8]
    MOM = [-6.8, 0, 1.4]
    CROWD_A = [-8.4, 0, -7.6]
    CROWD_B = [8.4, 0, -7.6]

    MAYA_RUN = [-4.8, 0, 3.4]
    JUNE_FALL = [4.8, 0, 1.0]
    DEX_RUN = [0, 0, 4.6]
    DEX_GATE = [6.6, 0, 5.6]
    MAYA_TURN = [-4.8, 0, 1.8]
    MAYA_GATE = [-3.0, 0, 3.6]
    MAYA_WIN = [-2.0, 0, 6.0]
    MOM_WIN = [3.4, 0, 5.4]

    S0 = 0
    S1 = 90
    S2 = B["b6"] - 1
    S3 = B["b8"] - 1
    S4 = B["b12"] - 1
    S5 = B["b16"] - 1
    S6 = B["b17"] - 1

    def sign_close(a, b):
        return shot(a, b, [0, 10.3, 9.6], [0, 10.0, 8.6],
                    [0, 9.9, -11.3], [0, 9.9, -11.3], 52)

    def race_front(a, b):
        return shot(a, b, [-4.8, 2.0, 13.0], [-4.8, 2.2, 11.5],
                    [-4.8, 3.2, 1.0], [-4.8, 3.4, 1.0], 46)

    def race_back(a, b):
        return shot(a, b, [0, 7.0, 16.0], [0, 6.8, 14.5],
                    [0, 4.0, 0.0], [0, 4.0, 0.5], 56)

    def june_run_close(a, b):
        return shot(a, b, [4.8, 4.9, 7.5], [4.8, 4.7, 6.5],
                    [4.8, 3.6, 1.0], [4.8, 3.6, 1.0], 44)

    def gate_wide(a, b):
        return wide(a, b, [0, 0, 2.0], dist=20.0, fov=58)

    def gate_mid(a, b):
        return medium(a, b, [0, 0, 2.0], dist=16.0, fov=55)

    def night_wide(a, b):
        return wide(a, b, [-1.5, 0, 4.0], dist=19.0, fov=58, push=2.0)

    def mom_close(a, b):
        return shot(a, b, [MOM_WIN[0] - 5.2, 4.9, MOM_WIN[2] + 3.2],
                    [MOM_WIN[0] - 4.6, 4.7, MOM_WIN[2] + 2.6],
                    [MOM_WIN[0], 4.3, MOM_WIN[2]], [MOM_WIN[0], 4.3, MOM_WIN[2]], 46)

    def june_night_med(a, b):
        return shot(a, b, [-8.0, 5.2, 4.6], [-7.4, 5.0, 4.0],
                    [-1.5, 4.2, 2.2], [-1.5, 4.2, 2.2], 48)

    def june_night_close(a, b):
        return shot(a, b, [-4.0, 5.0, 7.2], [-3.7, 4.9, 6.6],
                    [-2.0, 4.3, 2.2], [-2.0, 4.3, 2.2], 42)

    def maya_night_close(a, b):
        return shot(a, b, [-4.0, 4.9, 9.6], [-3.6, 4.7, 9.0],
                    [1.0, 4.2, 6.8], [1.0, 4.2, 6.8], 44)

    return [
        {
            "id": "s00-town",
            "location": "town_overview",
            "startFrame": S0,
            "endFrame": S1,
            "cameraShots": [
                shot(S0, S1, [-10, 62, 74], [-2, 47, 57], [8, 0, -6], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {
            "id": "s01-start-line",
            "location": "school_exterior",
            "schoolName": "ONE TICKET OUT",
            "startFrame": S1,
            "endFrame": S2,
            "cameraShots": cover(S1, S2, [
                lambda a, b: wide(a, b, [0, 0, -1.0], dist=24.0, fov=60),
                lambda a, b: sign_close(a, b),
                lambda a, b: medium(a, b, [0, 0, -5.0], dist=14.0, fov=52),
                lambda a, b: close_up(a, b, MAYA),
            ]),
            "characters": {
                "maya": hold(S1, S2, MAYA, 0.0, "idle", "deadpan"),
                "june": hold(S1, S2, JUNE_P, 0.0, "idle", "smile"),
                "dex": hold(S1, S2, DEX, 0.0, "idle", "cool"),
                "host": hold(S1, S2, HOST, face(HOST, [0, 0, -4]), "wave", "smile", "pointer"),
                "mom": [
                    kf(S1, MOM, 0.0, "idle", "deadpan"),
                    kf(B["b3"], MOM, 0.0, "panting", "deadpan"),
                    kf(S2, MOM, 0.0, "panting", "deadpan"),
                ],
                "crowd_a": hold(S1, S2, CROWD_A, face(CROWD_A, [0, 0, -4]), "idle", "smile"),
                "crowd_b": hold(S1, S2, CROWD_B, face(CROWD_B, [0, 0, -4]), "idle", "smile"),
            },
        },
        {
            "id": "s02-race",
            "location": "school_exterior",
            "schoolName": "ONE TICKET OUT",
            "startFrame": S2,
            "endFrame": S3,
            "cameraShots": split_shots(S2, S3, [
                lambda a, b: race_back(a, b),
                lambda a, b: race_front(a, b),
                lambda a, b: june_run_close(a, b),
                lambda a, b: wide(a, b, [0, 0, 2.0], dist=20.0, fov=58),
            ]),
            "characters": {
                "maya": [
                    kf(S2, MAYA, 0.0, "sprint", "panic"),
                    kf(B["b7"] - 8, MAYA_RUN, 0.0, "sprint", "panic"),
                    kf(B["b7"] + 4, MAYA_RUN, 0.0, "idle", "shocked"),
                    kf(S3, MAYA_RUN, 0.0, "idle", "shocked"),
                ],
                "june": [
                    kf(S2, JUNE_P, 0.0, "sprint", "panic"),
                    kf(B["b7"] - 20, [4.8, 0, 0.4], 0.0, "sprint", "panic"),
                    kf(B["b7"] + 2, JUNE_FALL, 0.0, "panting", "panic"),
                    kf(S3, JUNE_FALL, 0.0, "panting", "panic"),
                ],
                "dex": [
                    kf(S2, DEX, 0.0, "sprint", "cool"),
                    kf(S3, [0, 0, -2.0], 0.0, "sprint", "cool"),
                ],
            },
        },
        {
            "id": "s03-turn-back",
            "location": "school_exterior",
            "schoolName": "ONE TICKET OUT",
            "startFrame": S3,
            "endFrame": S4,
            "cameraShots": [
                gate_wide(S3, B["b9"] - 1),
                gate_mid(B["b9"] - 1, B["b10"] - 1),
                close_up(B["b10"] - 1, B["b11"] - 1, DEX_RUN, side=-1.6, dist=6.5, shake=0.05),
                close_up(B["b11"] - 1, S4, MAYA_TURN, side=2.5, dist=6.0, shake=0.04),
            ],
            "characters": {
                "maya": [
                    kf(S3, MAYA_RUN, 0.0, "idle", "shocked"),
                    kf(B["b8"] + 6, MAYA_TURN, 0.9, "idle", "panic"),
                    kf(S4, MAYA_TURN, 0.9, "idle", "panic"),
                ],
                "june": hold(S3, S4, JUNE_FALL, 0.0, "panting", "panic"),
                "dex": [
                    kf(S3, [0, 0, -2.0], 0.0, "sprint", "cool"),
                    kf(B["b9"] + 30, DEX_RUN, 0.0, "sprint", "cool"),
                    kf(B["b10"] - 4, DEX_RUN, -1.1, "point", "angry"),
                    kf(S4, DEX_RUN, -1.1, "idle", "deadpan"),
                ],
            },
        },
        {
            "id": "s04-gate-choice",
            "location": "school_exterior",
            "schoolName": "ONE TICKET OUT",
            "startFrame": S4,
            "endFrame": S5,
            "cameraShots": [
                medium(S4, B["b13"] - 1, DEX_GATE, dist=9.0, fov=46),
                close_up(B["b13"] - 1, B["b14"] - 1, MAYA_GATE),
                close_up(B["b14"] - 1, B["b15"] - 1, JUNE_FALL, dist=5.4, side=-3.4),
                gate_wide(B["b15"] - 1, S5),
            ],
            "characters": {
                "maya": [
                    kf(S4, MAYA_TURN, 0.9, "idle", "panic"),
                    kf(B["b15"] - 10, MAYA_GATE, 0.0, "walk", "deadpan"),
                    kf(S5, MAYA_GATE, 0.0, "idle", "deadpan"),
                ],
                "june": [
                    kf(S4, JUNE_FALL, 0.0, "panting", "panic"),
                    kf(B["b14"], JUNE_FALL, face(JUNE_FALL, MAYA_GATE), "idle", "smile"),
                    kf(S5, JUNE_FALL, face(JUNE_FALL, MAYA_GATE), "idle", "smile"),
                ],
                "dex": hold(S4, S5, DEX_GATE, -1.2, "idle", "deadpan"),
            },
        },
        {
            "id": "s05-win",
            "location": "school_exterior",
            "schoolName": "ONE TICKET OUT",
            "startFrame": S5,
            "endFrame": S6,
            "cameraShots": split_shots(S5, S6, [
                lambda a, b: medium(a, b, [-1.5, 0, 4.8], dist=10.0, fov=48),
                lambda a, b: mom_close(a, b),
            ]),
            "characters": {
                "maya": [
                    kf(S5, MAYA_GATE, 0.0, "walk", "deadpan"),
                    kf(B["b16"] + 18, MAYA_WIN, 0.0, "idle", "smile"),
                    kf(S6, MAYA_WIN, 0.0, "idle", "smile"),
                ],
                "mom": hold(S5, S6, MOM_WIN, face(MOM_WIN, MAYA_WIN), "wave", "smile"),
            },
        },
        {
            "id": "s06-night",
            "location": "street",
            "isNight": True,
            "startFrame": S6,
            "endFrame": END,
            "cameraShots": [
                night_wide(S6, S6 + 34),
                june_night_med(S6 + 34, B["b18"] - 1),
                june_night_close(B["b18"] - 1, B["b18"] + 34),
                maya_night_close(B["b18"] + 34, B["b19"] - 1),
                night_wide(B["b19"] - 1, B["b19"] + 40),
                night_wide(B["b19"] + 40, END),
            ],
            "characters": {
                "maya": hold(S6, END, [1.0, 0, 6.8], -0.4, "idle", "deadpan"),
                "june_night": [
                    kf(S6, [2.5, 0, 1.2], -HALF, "walk", "deadpan", "backpack"),
                    kf(B["b18"] - 8, [-1.5, 0, 2.2], -HALF, "walk", "deadpan", "backpack"),
                    kf(B["b18"], [-2.0, 0, 2.2], face([-2.0, 0, 2.2], [1.0, 0, 6.8]),
                       "idle", "deadpan", "backpack"),
                    kf(B["b19"] - 6, [-5.0, 0, 2.2], -HALF, "walk", "deadpan", "backpack"),
                    kf(END, [-8.5, 0, 2.2], -HALF, "idle", "deadpan", "backpack"),
                ],
            },
        },
    ]
