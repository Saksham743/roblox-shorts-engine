"""THE SCHOOL WHERE THE CHALKBOARD COMES TRUE"""
import math

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide

TITLE = "THE SCHOOL WHERE THE CHALKBOARD COMES TRUE"

BEATS = [
    {"id": "b1", "text": "In this town, whatever the teacher writes on the chalkboard comes true.", "pause": 0.14},
    {"id": "b2", "text": "Our teacher, Mrs. Vale, writes one rule every single morning.", "pause": 0.08},
    {"id": "b3", "text": "Last week she wrote NO TALKING, and the room went silent.", "pause": 0.10},
    {"id": "b4", "text": "Then she wrote EVERYONE DANCES, and nobody could stop dancing.", "pause": 0.10},
    {"id": "w1", "text": "DANCE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "b5", "text": "Nobody ever touches the chalk, and nobody erases that board.", "pause": 0.08},
    {"id": "b6", "text": "But my little brother Noah was so tired, he fell asleep standing up.", "pause": 0.12},
    {"id": "b7", "text": "Mrs. Vale smiled and wrote one soft word: SLEEP.", "pause": 0.12},
    {"id": "b8", "text": "Noah woke up, marched to the board, and wiped it away.", "pause": 0.10},
    {"id": "b9", "text": "The board went black, then the chalk started writing by itself.", "pause": 0.14},
    {"id": "w2", "text": "NOAH!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "b10", "text": "It wrote NOAH, then DETENTION, then one last word: FOREVER.", "pause": 0.16},
    {"id": "b11", "text": "Next morning, Noah's seat was empty, and nobody remembered him.", "pause": 0.16},
    {"id": "b12", "text": "I ran outside, and the school sign now read NOAH WHO?", "pause": 0.12},
    {"id": "b13", "text": "So I grabbed the chalk and wrote the only thing I had left.", "pause": 0.12},
    {"id": "b14", "text": "The board answered slowly: ONLY THE TEACHER WRITES.", "pause": 0.16},
    {"id": "w3", "text": "ERASE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "b15", "text": "So I erased every rule, one chalk line at a time.", "pause": 0.10},
    {"id": "b16", "text": "Noah walked back in, every word disappeared, and one line appeared: TODAY'S RULE. What would you write?", "pause": 0.30},
]

MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b9", "b10.end"), ("b14", "w3.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "swish"),
    ("b3", "bell_low"),
    ("b4", "pop", {"f": 760}),
    ("w1", "impact"),
    ("b5", "pop_down"),
    ("b6", "pop", {"f": 420}),
    ("b7+0.6", "swish"),
    ("b8", "swish", {"dur": 0.5}),
    ("b9", "riser", {"dur": 1.8}),
    ("w2", "impact"),
    ("b10+0.2", "bell_low"),
    ("b11", "sad"),
    ("b12", "pop", {"f": 480}),
    ("b13+0.5", "swish"),
    ("b14", "bell_low"),
    ("w3", "impact"),
    ("b15", "swish", {"dur": 0.5}),
    ("b16", "sparkle"),
    ("b16.end-0.5", "twist"),
]

CAST = {
    "hero": {
        "extends": "kid_boy",
        "skin": "light",
        "hair": {"style": "messyFringe", "color": "darkBrown"},
        "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
        "bottom": {"style": "jeans", "color": "denim"},
        "shoes": {"color": "white", "sole": "white"},
    },
    "noah": {
        "extends": "little_brother",
        "hair": {"style": "curly", "color": "ginger"},
        "top": {"style": "pullover", "color": "green", "secondary": "white"},
        "scale": 0.8,
    },
    "teacher": {
        "extends": "teacher_woman",
        "hair": {"style": "bun", "color": "gray"},
        "top": {"style": "blouse", "color": "purple", "secondary": "white"},
        "bottom": {"style": "skirt", "color": "charcoal"},
        "accessories": ["glasses"],
    },
}


def scenes(T):
    B, E, END = T.B, T.E, T.END
    S = [0] + [B[i] - 1 for i in ("b2", "b4", "b5", "b7", "b8", "b9", "b10",
                                        "b11", "b12", "b13", "b14", "b15", "b16")] + [END]

    HERO_AISLE = [-1.8, 0, 1.4]
    NOAH_BACK = [1.8, 0, 4.9]
    HERO_DANCE = [-0.9, 0, -2.2]
    NOAH_DANCE = [0.9, 0, 2.4]
    NOAH_ERASE = [-1.0, 0, -4.8]
    HERO_BOARD = [-1.2, 0, -4.6]
    HERO_WATCH = [-1.6, 0, 1.4]
    HERO_SHOCK = [-1.6, 0, -3.2]
    HERO_ERASE = [-1.0, 0, -4.6]
    HERO_FINAL = [-0.8, 0, -5.2]
    NOAH_FINAL = [4.0, 0, -5.2]
    TEACH = [5.2, 0, -5.0]
    TEACH_RY = face(TEACH, [0, 6.6, -7.95])

    def board_shot(a, b, z=4.0, fov=46, y=6.9):
        return shot(a, b, [0, y + 0.5, z], [0, y + 0.25, z - 1.2], [0, y, -7.9], [0, y, -7.9], fov)

    def board_wide(a, b):
        return shot(a, b, [0, 8.2, 18.5], [0, 7.9, 16.2], [0, 7.0, -7.9], [0, 7.0, -7.9], 50)

    def aerial(a, b, dx=-10):
        return shot(a, b, [dx, 62, 74], [dx + 5, 55, 64], [8, 0, -6], [5, 1, -7], 55)

    def class_wide(a, b):
        return wide(a, b, [0, 0, 0.5], dist=20.0, fov=58)

    def sign_close(a, b):
        return shot(a, b, [0, 10.3, 9.6], [0, 10.0, 8.6], [0, 9.9, -11.3], [0, 9.9, -11.3], 52)

    return [
        {
            "id": "s01-hook",
            "location": "town_overview",
            "startFrame": S[0],
            "endFrame": S[1],
            "cameraShots": split_shots(S[0], S[1], [
                lambda a, b: aerial(a, b, -10),
                lambda a, b: aerial(a, b, -5),
            ]),
            "characters": {},
        },
        {
            "id": "s02-no-talking",
            "location": "classroom",
            "boardText": ["NO TALKING"],
            "startFrame": S[1],
            "endFrame": S[2],
            "cameraShots": cover(S[1], S[2], [
                lambda a, b: class_wide(a, b),
                lambda a, b: board_shot(a, b, z=6.5, fov=46),
                lambda a, b: close_up(a, b, HERO_AISLE),
                lambda a, b: close_up(a, b, TEACH, side=2.2),
            ]),
            "characters": {
                "teacher": [
                    kf(S[1], TEACH, TEACH_RY, "wave", "deadpan", "pointer"),
                    kf(B["b3"], TEACH, 0.15, "idle", "deadpan", "pointer"),
                    kf(S[2], TEACH, 0.15, "idle", "deadpan", "pointer"),
                ],
                "hero": hold(S[1], S[2], HERO_AISLE, 0.1, "idle", "deadpan"),
                "noah": hold(S[1], S[2], NOAH_BACK, 0.1, "idle", "deadpan"),
            },
        },
        {
            "id": "s03-dance-rule",
            "location": "classroom",
            "boardText": ["EVERYONE DANCES!"],
            "startFrame": S[2],
            "endFrame": S[3],
            "cameraShots": cover(S[2], S[3], [
                lambda a, b: class_wide(a, b),
                lambda a, b: close_up(a, b, HERO_DANCE),
                lambda a, b: close_up(a, b, NOAH_DANCE, scale=0.8),
                lambda a, b: medium(a, b, TEACH, dist=12.0, fov=50),
            ]),
            "characters": {
                "hero": hold(S[2], S[3], HERO_DANCE, 0.0, "dance", "laugh"),
                "noah": hold(S[2], S[3], NOAH_DANCE, 0.0, "dance", "laugh"),
                "teacher": hold(S[2], S[3], TEACH, 0.15, "dance", "deadpan", "pointer"),
            },
        },
        {
            "id": "s04-noah-tired",
            "location": "classroom",
            "boardText": ["EVERYONE DANCES!"],
            "startFrame": S[3],
            "endFrame": S[4],
            "cameraShots": cover(S[3], S[4], [
                lambda a, b: class_wide(a, b),
                lambda a, b: close_up(a, b, HERO_AISLE),
                lambda a, b: close_up(a, b, NOAH_BACK, scale=0.8),
            ]),
            "characters": {
                "hero": hold(S[3], S[4], HERO_AISLE, 0.1, "idle", "deadpan"),
                "noah": hold(S[3], S[4], NOAH_BACK, 0.1, "sleep", "sleeping"),
            },
        },
        {
            "id": "s05-sleep-written",
            "location": "classroom",
            "boardText": ["SLEEP."],
            "startFrame": S[4],
            "endFrame": S[5],
            "cameraShots": split_shots(S[4], S[5], [
                lambda a, b: board_shot(a, b, z=5.0, fov=46),
                lambda a, b: close_up(a, b, NOAH_BACK, scale=0.8),
            ]),
            "characters": {
                "teacher": hold(S[4], S[5], TEACH, TEACH_RY, "wave", "smile", "pointer"),
                "noah": hold(S[4], S[5], NOAH_BACK, 0.1, "sleep", "sleeping"),
            },
        },
        {
            "id": "s06-noah-erases",
            "location": "classroom",
            "boardText": [],
            "startFrame": S[5],
            "endFrame": S[6],
            "cameraShots": split_shots(S[5], S[6], [
                lambda a, b: class_wide(a, b),
                lambda a, b: medium(a, b, [0.0, 0, -4.6], dist=10.0, fov=52),
            ]),
            "characters": {
                "teacher": hold(S[5], S[6], TEACH, 0.15, "idle", "deadpan", "pointer"),
                "noah": [
                    kf(S[5], NOAH_BACK, 0.0, "sleep", "sleeping"),
                    kf(S[5] + 12, NOAH_BACK, 0.0, "idle", "panic"),
                    kf(S[5] + 20, NOAH_BACK, math.pi, "walk", "panic"),
                    kf(S[6] - 25, NOAH_ERASE, math.pi, "walk", "panic"),
                    kf(S[6] - 10, NOAH_ERASE, TEACH_RY, "wave", "panic"),
                    kf(S[6], NOAH_ERASE, TEACH_RY, "wave", "panic"),
                ],
            },
        },
        {
            "id": "s07-name-appears",
            "location": "classroom",
            "boardText": ["NOAH!"],
            "startFrame": S[6],
            "endFrame": S[7],
            "cameraShots": cover(S[6], S[7], [
                lambda a, b: board_shot(a, b, z=4.6, fov=46),
                lambda a, b: close_up(a, b, NOAH_ERASE),
                lambda a, b: close_up(a, b, TEACH, side=2.2),
            ]),
            "characters": {
                "noah": hold(S[6], S[7], NOAH_ERASE, 0.0, "idle", "shocked"),
                "teacher": hold(S[6], S[7], TEACH, 0.15, "idle", "deadpan", "pointer"),
            },
        },
        {
            "id": "s08-forever",
            "location": "classroom",
            "boardText": ["NOAH!", "DETENTION!", "FOREVER!"],
            "startFrame": S[7],
            "endFrame": S[8],
            "cameraShots": [
                shot(S[7], B["b10"] + 35, [0, 8.0, 19.0], [0, 7.8, 17.0], [0, 6.2, -5.0], [0, 6.3, -5.0], 55),
                shot(B["b10"] + 35, S[8], [HERO_WATCH[0] + 2.2, 5.2, HERO_WATCH[2] + 7.0],
                     [HERO_WATCH[0] + 1.8, 5.0, HERO_WATCH[2] + 5.8], [HERO_WATCH[0], 4.4, HERO_WATCH[2]],
                     [HERO_WATCH[0], 4.4, HERO_WATCH[2]], 46),
            ],
            "characters": {
                "hero": [
                    kf(S[7], HERO_WATCH, 0.0, "idle", "panic"),
                    kf(B["b10"] + 36, HERO_WATCH, 0.0, "idle", "shocked"),
                    kf(S[8], HERO_WATCH, 0.0, "idle", "shocked"),
                ],
                "noah": [
                    kf(S[7], NOAH_ERASE, 0.0, "idle", "panic"),
                    kf(B["b10"] + 35, NOAH_ERASE, 0.0, "idle", "shocked"),
                    kf(B["b10"] + 36, OFF, 0.0, "idle", "shocked"),
                ],
                "teacher": hold(S[7], S[8], TEACH, 0.15, "idle", "deadpan", "pointer"),
            },
        },
        {
            "id": "s09-empty-seat",
            "location": "classroom",
            "boardText": [],
            "startFrame": S[8],
            "endFrame": S[9],
            "cameraShots": split_shots(S[8], S[9], [
                lambda a, b: class_wide(a, b),
                lambda a, b: shot(a, b, [5.5, 4.6, 8.0], [5.5, 4.3, 6.8], [5.5, 2.4, 0.5], [5.5, 2.4, 0.5], 48),
            ]),
            "characters": {
                "hero": hold(S[8], S[9], HERO_WATCH, 0.0, "idle", "deadpan"),
            },
        },
        {
            "id": "s10-noah-who",
            "location": "school_exterior",
            "schoolName": "NOAH WHO?",
            "startFrame": S[9],
            "endFrame": S[10],
            "cameraShots": split_shots(S[9], S[10], [
                lambda a, b: wide(a, b, [0, 0, 2.0], dist=22.0, fov=60),
                lambda a, b: sign_close(a, b),
            ]),
            "characters": {
                "hero": hold(S[9], S[10], [-2.5, 0, 3.0], 0.0, "panting", "panic"),
            },
        },
        {
            "id": "s11-he-writes",
            "location": "classroom",
            "boardText": ["NOAH COMES BACK"],
            "startFrame": S[10],
            "endFrame": S[11],
            "cameraShots": split_shots(S[10], S[11], [
                lambda a, b: board_shot(a, b, z=16.0, fov=48),
                lambda a, b: close_up(a, b, HERO_BOARD),
            ]),
            "characters": {
                "hero": hold(S[10], S[11], HERO_BOARD, 0.0, "wave", "panic"),
            },
        },
        {
            "id": "s12-only-teacher",
            "location": "classroom",
            "boardText": ["ONLY THE TEACHER WRITES."],
            "startFrame": S[11],
            "endFrame": S[12],
            "cameraShots": split_shots(S[11], S[12], [
                lambda a, b: board_wide(a, b),
                lambda a, b: close_up(a, b, HERO_SHOCK),
            ]),
            "characters": {
                "hero": hold(S[11], S[12], HERO_SHOCK, 0.0, "idle", "shocked"),
                "teacher": hold(S[11], S[12], TEACH, 0.15, "idle", "deadpan", "pointer"),
            },
        },
        {
            "id": "s13-erase-everything",
            "location": "classroom",
            "boardText": ["ONLY THE TEACHER WRITES."],
            "startFrame": S[12],
            "endFrame": S[13],
            "cameraShots": split_shots(S[12], S[13], [
                lambda a, b: medium(a, b, HERO_ERASE, dist=11.0, fov=52),
                lambda a, b: class_wide(a, b),
            ]),
            "characters": {
                "hero": hold(S[12], S[13], HERO_ERASE, -HALF, "wave", "angry"),
                "teacher": hold(S[12], S[13], TEACH, 0.15, "idle", "shocked", "pointer"),
            },
        },
        {
            "id": "s14-your-rule",
            "location": "classroom",
            "boardText": ["TODAY'S RULE:", "________"],
            "startFrame": S[13],
            "endFrame": S[14],
            "cameraShots": [
                shot(S[13], B["b16"] + 40, [1.6, 5.8, 13.0], [1.6, 5.6, 11.8], [1.2, 4.3, -5.2], [1.2, 4.3, -5.2], 54),
                shot(B["b16"] + 40, B["b16"] + 100, [NOAH_FINAL[0] + 1.4, 4.6, 2.4],
                     [NOAH_FINAL[0] + 1.1, 4.4, 1.2], [NOAH_FINAL[0], 3.6, NOAH_FINAL[2]],
                     [NOAH_FINAL[0], 3.6, NOAH_FINAL[2]], 44),
                shot(B["b16"] + 100, S[14], [HERO_FINAL[0] + 1.2, 5.2, 1.6], [HERO_FINAL[0] + 0.9, 5.0, 0.6],
                     [HERO_FINAL[0], 4.4, HERO_FINAL[2]], [HERO_FINAL[0], 4.4, HERO_FINAL[2]], 46),
            ],
            "characters": {
                "hero": [
                    kf(S[13], HERO_FINAL, 0.0, "idle", "panic"),
                    kf(B["b16"] + 78, HERO_FINAL, 0.0, "idle", "smile"),
                    kf(B["b16"] + 80, HERO_FINAL, 0.0, "idle", "smile"),
                ],
                "noah": [
                    kf(S[13], OFF, 0.0, "idle", "shocked"),
                    kf(B["b16"] + 14, OFF, 0.0, "idle", "shocked"),
                    kf(B["b16"] + 15, NOAH_FINAL, 0.0, "idle", "shocked"),
                    kf(B["b16"] + 78, NOAH_FINAL, 0.0, "idle", "smile"),
                    kf(B["b16"] + 80, NOAH_FINAL, 0.0, "idle", "smile"),
                ],
            },
        },
    ]
