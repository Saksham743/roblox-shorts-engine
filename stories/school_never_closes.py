
from shorts.scene import (
    HALF, OFF, hold, kf, shot,
    wide, medium, close_up, cover, split_shots
)

TITLE = "THE SCHOOL THAT NEVER CLOSES"

BEATS = [
    {"id": "b1", "text": "In this town, our school has been abandoned for ten years.", "pause": 0.08},
    {"id": "b2", "text": "But every night at exactly 3 AM, one classroom lights up.", "pause": 0.10},
    {"id": "b3", "text": "Nobody has ever been brave enough to enter.", "pause": 0.08},
    {"id": "b4", "text": "Until one night, I saw someone standing inside.", "pause": 0.10},
    {"id": "b5", "text": "I walked through the unlocked school entrance.", "pause": 0.08},
    {"id": "b6", "text": "Every hallway was completely empty.", "pause": 0.08},
    {"id": "b7", "text": "But I could hear a teacher taking attendance.", "pause": 0.10},
    {"id": "b8", "text": "When I reached the classroom, every student was facing the board.", "pause": 0.10},
    {"id": "b9", "text": "The teacher suddenly stopped speaking.", "pause": 0.10},
    {"id": "b10", "text": "Then he slowly turned toward me.", "pause": 0.10},
    {"id": "b11", "text": 'He said, "You are late. We have been waiting."', "pause": 0.12},
    {"id": "b12", "text": "Every student turned around at the exact same time.", "pause": 0.12},
    {"id": "b13", "text": "I ran toward the exit, but the door would not open.", "pause": 0.10},
    {"id": "b14", "text": "Then I read the rule written on the blackboard.", "pause": 0.10},
    {"id": "b15", "text": "Rule number one. Be on time.", "pause": 0.18},
    {"id": "b16", "text": 'And behind me, the teacher whispered, "Take your seat."', "pause": 0.25},
]

MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b15", "b16.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b2", "bell_low"),
    ("b4", "thud"),
    ("b7", "bell_low"),
    ("b9", "twist"),
    ("b10", "riser", {"dur": 1.5}),
    ("b11", "impact"),
    ("b12", "twist"),
    ("b13", "whoosh"),
    ("b14", "thud"),
    ("b15", "bell_low"),
    ("b16", "reveal"),
]

# Main protagonist
HERO = {
    "skin": "classic",
    "hair": {"style": "messyFringe", "color": "darkBrown"},
    "top": {"style": "hoodie", "color": "black", "secondary": "gray"},
    "bottom": {"style": "jeans", "color": "charcoal"},
    "shoes": {"style": "sneakers", "color": "white"},
}

# Teacher
TEACHER = {
    "skin": "classic",
    "hair": {"style": "messyFringe", "color": "black"},
    "top": {"style": "hoodie", "color": "darkRed", "secondary": "black"},
    "bottom": {"style": "pants", "color": "black"},
    "shoes": {"style": "sneakers", "color": "black"},
}

# Two students
STUDENT = {
    "skin": "classic",
    "hair": {"style": "messyFringe", "color": "black"},
    "top": {"style": "hoodie", "color": "blue", "secondary": "black"},
    "bottom": {"style": "jeans", "color": "black"},
    "shoes": {"style": "sneakers", "color": "white"},
}

STUDENT_TWO = {
    "skin": "dark",
    "hair": {"style": "messyFringe", "color": "black"},
    "top": {"style": "hoodie", "color": "gray", "secondary": "black"},
    "bottom": {"style": "jeans", "color": "charcoal"},
    "shoes": {"style": "sneakers", "color": "black"},
}

CAST = {
    "hero": HERO,
    "teacher": TEACHER,
    "student_one": STUDENT,
    "student_two": STUDENT_TWO,
}


def scenes(T):
    B, END = T.B, T.END

    # Scene boundaries
    S2 = B["b4"] - 1
    S3 = B["b8"] - 1
    S4 = B["b13"] - 1

    # Character positions
    HERO_P = [-4.0, 0, 1.5]
    TEACHER_P = [4.0, 0, 1.5]

    STUDENT_ONE_P = [-1.0, 0, -4.0]
    STUDENT_TWO_P = [5.0, 0, -4.0]

    HALL_TEACHER_P = [2.5, 0, -4.0]
    FINAL_TEACHER_P = [-1.5, 0, -3.5]

    return [
        # --------------------------------------------------
        # SCENE 1: THE ABANDONED SCHOOL
        # Beats 1-3
        # --------------------------------------------------
        {
            "id": "school-opening",
            "location": "school_exterior",
            "isNight": True,
            "startFrame": 0,
            "endFrame": S2,

            "cameraShots": split_shots(
                0, S2,
                [
                    lambda a, b: shot(
                        a, b,
                        [-10, 62, 74], [-5, 55, 65],
                        [8, 0, -6], [8, 0, -6], 55
                    ),
                    lambda a, b: shot(
                        a, b,
                        [-5, 55, 65], [2, 48, 58],
                        [8, 0, -6], [8, 0, -6], 55
                    ),
                    lambda a, b: shot(
                        a, b,
                        [2, 48, 58], [8, 42, 52],
                        [8, 0, -6], [8, 0, -6], 55
                    ),
                ],
            ),

            "characters": {},
        },

        # --------------------------------------------------
        # SCENE 2: THE EMPTY HALLWAY
        # Beats 4-7
        # --------------------------------------------------
        {
            "id": "empty-hallway",
            "location": "hallway",
            "isNight": True,
            "startFrame": S2,
            "endFrame": S3,

            "cameraShots": cover(
                S2, S3,
                [
                    lambda a, b: wide(a, b),
                    lambda a, b: medium(a, b, HERO_P),
                    lambda a, b: close_up(a, b, HERO_P),
                ],
            ),

            "characters": {
                "hero": [
                    kf(S2, HERO_P, 0, "walk", "shocked"),
                    kf(B["b5"], HERO_P, 0, "walk", "panic"),
                    kf(B["b6"], HERO_P, 0, "idle", "shocked"),
                    kf(B["b7"], HERO_P, 0, "idle", "panic"),
                    kf(S3, HERO_P, 0, "idle", "panic"),
                ],

                "teacher": [
                    kf(S2, HALL_TEACHER_P, 180, "idle", "deadpan"),
                    kf(B["b5"], HALL_TEACHER_P, 180, "idle", "deadpan"),
                    kf(B["b7"], HALL_TEACHER_P, 180, "idle", "deadpan"),
                    kf(S3, HALL_TEACHER_P, 180, "idle", "deadpan"),
                ],
            },
        },

        # --------------------------------------------------
        # SCENE 3: THE CLASSROOM
        # Beats 8-12
        # --------------------------------------------------
        {
            "id": "classroom-reveal",
            "location": "classroom",
            "isNight": True,
            "startFrame": S3,
            "endFrame": S4,

            "cameraShots": cover(
                S3, S4,
                [
                    lambda a, b: wide(a, b),
                    lambda a, b: medium(a, b, HERO_P),
                    lambda a, b: close_up(a, b, TEACHER_P),
                ],
            ),

            "characters": {
                "hero": [
                    kf(S3, HERO_P, 0, "walk", "shocked"),
                    kf(B["b9"], HERO_P, 0, "idle", "shocked"),
                    kf(B["b10"], HERO_P, 0, "idle", "panic"),
                    kf(B["b11"], HERO_P, 0, "idle", "panic"),
                    kf(S4, HERO_P, 0, "idle", "panic"),
                ],

                "teacher": [
                    kf(S3, TEACHER_P, 180, "idle", "deadpan"),
                    kf(B["b9"], TEACHER_P, 180, "idle", "deadpan"),
                    kf(B["b10"], TEACHER_P, 0, "idle", "angry"),
                    kf(B["b11"], TEACHER_P, 0, "point", "deadpan"),
                    kf(S4, TEACHER_P, 0, "idle", "deadpan"),
                ],

                "student_one": [
                    kf(S3, STUDENT_ONE_P, 180, "idle", "deadpan"),
                    kf(B["b12"], STUDENT_ONE_P, 0, "idle", "shocked"),
                    kf(S4, STUDENT_ONE_P, 0, "idle", "deadpan"),
                ],

                "student_two": [
                    kf(S3, STUDENT_TWO_P, 180, "idle", "deadpan"),
                    kf(B["b12"], STUDENT_TWO_P, 0, "idle", "shocked"),
                    kf(S4, STUDENT_TWO_P, 0, "idle", "deadpan"),
                ],
            },
        },

        # --------------------------------------------------
        # SCENE 4: THE FINAL CLASS
        # Beats 13-16
        # --------------------------------------------------
        {
            "id": "final-class",
            "location": "classroom",
            "isNight": True,
            "startFrame": S4,
            "endFrame": END,

            "cameraShots": cover(
                S4, END,
                [
                    lambda a, b: wide(a, b),
                    lambda a, b: medium(a, b, HERO_P),
                    lambda a, b: close_up(a, b, [2.5, 0, -2.5]),
                ],
            ),
            "characters": {
                "hero": [
                    kf(S4, HERO_P, 0, "sprint", "panic"),
                    kf(B["b14"], [-1.5, 0, 1.5], 0, "idle", "shocked"),
                    kf(B["b15"], [-1.5, 0, 1.5], 0, "idle", "panic"),
                    kf(END, [-1.5, 0, 1.5], 180, "idle", "shocked"),
                ],

                "teacher": [
                    kf(S4, [2.5, 0, -2.5], 180, "idle", "deadpan"),
                    kf(B["b14"], [2.5, 0, -2.5], 180, "idle", "deadpan"),
                    kf(B["b15"], [2.5, 0, -2.5], 0, "point", "angry"),
                    kf(END, [2.5, 0, -2.5], 0, "idle", "deadpan"),
                ],

                "student_one": hold(
                    S4, END, [-6.0, 0, -4.0], 0, "idle", "deadpan"
                ),

                "student_two": hold(
                    S4, END, [6.0, 0, -6.0], 0, "idle", "deadpan"
                ),
            },
        },
    ]
