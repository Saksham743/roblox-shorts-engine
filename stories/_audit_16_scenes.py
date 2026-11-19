"""Temporary 16-scene scalability audit story. Not a production story."""
from shorts.scene import HALF, close_up, hold, kf, medium, shot, wide

TITLE = "THE TOWN THAT FORBADE WALKING"

BEATS = [
    {"id": "b1", "text": "In this town, nobody is allowed to walk anywhere. Not even one step.", "pause": 0.14},
    {"id": "b2", "text": "Everyone runs to school, to work, and even to breakfast.", "pause": 0.12},
    {"id": "b3", "text": "My best friend Mia runs every single step right beside me.", "pause": 0.12},
    {"id": "b4", "text": "We sprint the final block before the morning bell rings.", "pause": 0.12},
    {"id": "b5", "text": "The principal times every single student at the school gate.", "pause": 0.12},
    {"id": "b6", "text": "Take one slow step, and the hallway floor turns bright red.", "pause": 0.14},
    {"id": "b7", "text": "So the whole class sprints in place beside their little desks.", "pause": 0.12},
    {"id": "b8", "text": "Then one quiet morning, Mia stopped running completely.", "pause": 0.16},
    {"id": "b9", "text": "She walked slowly, right past the frozen and furious principal.", "pause": 0.14},
    {"id": "b10", "text": "The entire town went silent, and every single runner stopped.", "pause": 0.14},
    {"id": "b11", "text": "I walked beside her, and my heart pounded louder and louder.", "pause": 0.12},
    {"id": "b12", "text": "People pointed and whispered from behind the shop windows.", "pause": 0.12},
    {"id": "b13", "text": "The principal raised his silver whistle slowly to his lips.", "pause": 0.14},
    {"id": "b14", "text": "But then the bell rang, and nobody moved at all.", "pause": 0.16},
    {"id": "b15", "text": "That night, the whole town walked home together in silence.", "pause": 0.14},
    {"id": "b16", "text": "And in this town, walking became the brand new rule.", "pause": 0.30},
]

MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b13", "b14.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b2", "pop"),
    ("b3", "sparkle"),
    ("b4", "swish"),
    ("b5", "ding_dong"),
    ("b6", "thud"),
    ("b7", "pop", {"f": 720}),
    ("b8", "bell_low"),
    ("b9", "sad"),
    ("b10", "thud"),
    ("b11", "pop", {"f": 540}),
    ("b12", "pop", {"f": 660}),
    ("b13", "riser", {"dur": 1.2}),
    ("b14", "ding_dong"),
    ("b15", "reveal"),
    ("b16", "twist"),
]

CAST = {
    "hero": {
        "extends": "kid_boy",
        "hair": {"style": "messyFringe", "color": "black"},
        "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
        "bottom": {"style": "jeans", "color": "denim"},
        "shoes": {"color": "white", "sole": "white"},
    },
    "mia": {
        "extends": "kid_girl",
        "hair": {"style": "ponytail", "color": "blonde"},
        "top": {"style": "sweater", "color": "pink", "secondary": "white"},
        "bottom": {"style": "jeans", "color": "denim"},
        "shoes": {"color": "white", "sole": "pink"},
    },
    "principal": {
        "extends": "principal",
        "hair": {"style": "sidePart", "color": "gray"},
    },
}


def scenes(T):
    B, END = T.B, T.END
    S = [0] + [B[f"b{i}"] - 1 for i in range(2, 17)] + [END]

    HERO_P = [-3.0, 0, 1.0]
    MIA_P = [3.0, 0, 1.0]
    PRIN_P = [0.0, 0, 0.0]

    return [
        {
            "id": "s01-hook",
            "location": "town_overview",
            "startFrame": S[0],
            "endFrame": S[1],
            "cameraShots": [
                shot(S[0], S[0] + 56, [-10, 62, 74], [-6, 54, 66], [8, 0, -6], [4, 1, -7], 55),
                shot(S[0] + 56, S[1], [-6, 54, 66], [-2, 46, 56], [4, 1, -7], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {
            "id": "s02-run-to-breakfast",
            "location": "street",
            "startFrame": S[1],
            "endFrame": S[2],
            "cameraShots": [wide(S[1], S[2], [0, 0, 1.0], dist=24.0, fov=64)],
            "characters": {
                "hero": [
                    kf(S[1], [-6.0, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[2] - 8, [-1.0, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[2], [-1.0, 0, 1.0], 0.3, "idle", "smile"),
                ],
                "mia": hold(S[1], S[2], [4.5, 0, 1.0], 0.0, "wave", "smile"),
            },
        },
        {
            "id": "s03-best-friend",
            "location": "crossroads",
            "startFrame": S[2],
            "endFrame": S[3],
            "cameraShots": [medium(S[2], S[3], [0.5, 0, 1.2], dist=24.0, fov=62)],
            "characters": {
                "hero": [
                    kf(S[2], [-5.0, 0, 1.2], HALF, "walk", "smile"),
                    kf(S[3] - 6, [-2.0, 0, 1.2], HALF, "walk", "smile"),
                    kf(S[3], [-2.0, 0, 1.2], HALF, "idle", "smile"),
                ],
                "mia": [
                    kf(S[2], [0.0, 0, 1.2], HALF, "walk", "laugh"),
                    kf(S[3] - 6, [3.0, 0, 1.2], HALF, "walk", "laugh"),
                    kf(S[3], [3.0, 0, 1.2], HALF, "idle", "laugh"),
                ],
            },
        },
        {
            "id": "s04-final-block",
            "location": "playground",
            "startFrame": S[3],
            "endFrame": S[4],
            "cameraShots": [wide(S[3], S[4], [0, 0, 1.5], dist=24.0, fov=64)],
            "characters": {
                "hero": [
                    kf(S[3], [-6.0, 0, 1.5], HALF, "sprint", "smile"),
                    kf(S[4] - 6, [-1.0, 0, 1.5], HALF, "sprint", "smile"),
                    kf(S[4], [-1.0, 0, 1.5], HALF, "panting", "laugh"),
                ],
                "mia": [
                    kf(S[3], [-1.0, 0, 1.5], HALF, "sprint", "laugh"),
                    kf(S[4] - 6, [4.0, 0, 1.5], HALF, "sprint", "laugh"),
                    kf(S[4], [4.0, 0, 1.5], HALF, "panting", "laugh"),
                ],
            },
        },
        {
            "id": "s05-school-gate",
            "location": "school_exterior",
            "schoolName": "SPRINTVILLE SCHOOL",
            "startFrame": S[4],
            "endFrame": S[5],
            "cameraShots": [wide(S[4], S[5], [0, 0, 0.5], dist=22.0, fov=60)],
            "characters": {
                "hero": hold(S[4], S[5], [-4.5, 0, 1.0], 0.0, "panting", "panic"),
                "mia": hold(S[4], S[5], [4.5, 0, 1.0], 0.0, "panting", "panic"),
                "principal": hold(S[4], S[5], [0.0, 0, -1.0], 0.0, "idle", "deadpan", "clipboard"),
            },
        },
        {
            "id": "s06-red-floor",
            "location": "hallway",
            "startFrame": S[5],
            "endFrame": S[6],
            "cameraShots": [wide(S[5], S[6], [0, 0, 1.0])],
            "characters": {
                "hero": [
                    kf(S[5], [-3.0, 0, 1.0], HALF, "walk", "panic"),
                    kf(S[6] - 6, [-2.5, 0, 1.0], HALF, "walk", "panic"),
                    kf(S[6], [-2.5, 0, 1.0], 0.0, "idle", "shocked"),
                ],
                "mia": [
                    kf(S[5], [3.0, 0, 1.0], -HALF, "walk", "panic"),
                    kf(S[6] - 6, [2.5, 0, 1.0], -HALF, "walk", "panic"),
                    kf(S[6], [2.5, 0, 1.0], 0.0, "idle", "shocked"),
                ],
            },
        },
        {
            "id": "s07-sprint-in-place",
            "location": "classroom",
            "boardText": ["NO WALKING", "RUN TO RECESS", "RUN HOME", "RUN ALWAYS"],
            "startFrame": S[6],
            "endFrame": S[7],
            "cameraShots": [medium(S[6], S[7], [0, 0, 2.0], dist=24.0, fov=62)],
            "characters": {
                "hero": hold(S[6], S[7], [-3.0, 0, 2.0], 0.0, "sprint", "panic"),
                "mia": hold(S[6], S[7], [3.0, 0, 2.0], 0.0, "sprint", "panic"),
            },
        },
        {
            "id": "s08-mia-stops",
            "location": "school_exterior",
            "schoolName": "SPRINTVILLE SCHOOL",
            "startFrame": S[7],
            "endFrame": S[8],
            "cameraShots": [close_up(S[7], S[8], [0.0, 0, 1.0], scale=1.0)],
            "characters": {
                "hero": hold(S[7], S[8], [-5.0, 0, 1.0], 0.0, "idle", "shocked"),
                "mia": hold(S[7], S[8], [0.0, 0, 1.0], 0.0, "idle", "shocked"),
            },
        },
        {
            "id": "s09-past-principal",
            "location": "playground",
            "startFrame": S[8],
            "endFrame": S[9],
            "cameraShots": [wide(S[8], S[9], [-0.5, 0, 1.0], dist=22.0, fov=60)],
            "characters": {
                "principal": hold(S[8], S[9], [-5.0, 0, 0.5], 0.0, "idle", "angry", "clipboard"),
                "mia": [
                    kf(S[8], [0.0, 0, 1.0], HALF, "walk", "deadpan"),
                    kf(S[9] - 8, [4.0, 0, 1.0], HALF, "walk", "deadpan"),
                    kf(S[9], [4.0, 0, 1.0], HALF, "idle", "deadpan"),
                ],
            },
        },
        {
            "id": "s10-town-silent",
            "location": "crossroads",
            "startFrame": S[9],
            "endFrame": S[10],
            "cameraShots": [wide(S[9], S[10], [0, 0, 1.0])],
            "characters": {
                "hero": hold(S[9], S[10], [-3.0, 0, 1.0], 0.0, "idle", "shocked"),
                "mia": hold(S[9], S[10], [3.0, 0, 1.0], 0.0, "idle", "deadpan"),
            },
        },
        {
            "id": "s11-i-walk-too",
            "location": "street",
            "startFrame": S[10],
            "endFrame": S[11],
            "cameraShots": [medium(S[10], S[11], [0.5, 0, 1.0], dist=24.0, fov=62)],
            "characters": {
                "hero": [
                    kf(S[10], [-3.0, 0, 1.0], HALF, "walk", "panic"),
                    kf(S[11] - 6, [-0.5, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[11], [-0.5, 0, 1.0], HALF, "idle", "smile"),
                ],
                "mia": hold(S[10], S[11], [4.5, 0, 1.0], -HALF, "walk", "deadpan"),
            },
        },
        {
            "id": "s12-shop-whispers",
            "location": "shop",
            "startFrame": S[11],
            "endFrame": S[12],
            "cameraShots": [medium(S[11], S[12], [0.5, 0, 1.0], dist=24.0, fov=62)],
            "characters": {
                "hero": hold(S[11], S[12], [-2.0, 0, 1.0], 0.0, "idle", "deadpan"),
                "mia": hold(S[11], S[12], [3.0, 0, 1.0], 0.0, "idle", "deadpan"),
            },
        },
        {
            "id": "s13-the-whistle",
            "location": "school_exterior",
            "schoolName": "SPRINTVILLE SCHOOL",
            "startFrame": S[12],
            "endFrame": S[13],
            "cameraShots": [close_up(S[12], S[13], [0.0, 0, 0.0], scale=1.0)],
            "characters": {
                "hero": hold(S[12], S[13], [-4.5, 0, 1.0], 0.0, "idle", "panic"),
                "mia": hold(S[12], S[13], [4.5, 0, 1.0], 0.0, "idle", "panic"),
                "principal": hold(S[12], S[13], [0.0, 0, 0.0], 0.0, "point", "angry"),
            },
        },
        {
            "id": "s14-nobody-moves",
            "location": "hallway",
            "startFrame": S[13],
            "endFrame": S[14],
            "cameraShots": [wide(S[13], S[14], [0, 0, 1.0])],
            "characters": {
                "hero": hold(S[13], S[14], [-3.0, 0, 1.0], 0.0, "idle", "shocked"),
                "mia": hold(S[13], S[14], [3.0, 0, 1.0], 0.0, "idle", "shocked"),
            },
        },
        {
            "id": "s15-walk-home",
            "location": "house",
            "variant": "blue",
            "isNight": True,
            "startFrame": S[14],
            "endFrame": S[15],
            "cameraShots": [wide(S[14], S[15], [0, 0, 1.0])],
            "characters": {
                "hero": [
                    kf(S[14], [-3.0, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[15] - 6, [-1.0, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[15], [-1.0, 0, 1.0], HALF, "idle", "smile"),
                ],
                "mia": [
                    kf(S[14], [2.0, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[15] - 6, [4.0, 0, 1.0], HALF, "walk", "smile"),
                    kf(S[15], [4.0, 0, 1.0], HALF, "idle", "smile"),
                ],
            },
        },
        {
            "id": "s16-new-rule",
            "location": "living_room",
            "variant": "blue",
            "isNight": True,
            "startFrame": S[15],
            "endFrame": S[16],
            "cameraShots": [medium(S[15], S[16], [0, 0, 1.5], dist=24.0, fov=62)],
            "characters": {
                "hero": hold(S[15], S[16], [-3.0, 0, 1.5], 0.0, "idle", "smile"),
                "mia": hold(S[15], S[16], [3.0, 0, 1.5], 0.0, "idle", "smile"),
            },
        },
    ]
