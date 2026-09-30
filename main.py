import pygame
import random
import math
import json
import os

pygame.init()

# =========================================================
# NEON REVENGE - ULTIMATE LOBBY EDITION
# FIXED UPGRADES + REAL MULTI SHOT
# =========================================================

WIDTH = 1100
HEIGHT = 700
FPS = 60

# Fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("NEON REVENGE")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 20)
SMALL = pygame.font.SysFont("consolas", 16)
BIG = pygame.font.SysFont("consolas", 42, bold=True)
HUGE = pygame.font.SysFont("consolas", 65, bold=True)

WHITE = (240, 245, 255)
CYAN = (0, 230, 255)
BLUE = (50, 110, 255)
PURPLE = (190, 50, 255)
PINK = (255, 40, 150)
RED = (255, 65, 70)
GREEN = (50, 255, 130)
YELLOW = (255, 220, 60)
ORANGE = (255, 145, 40)

DARK = (7, 9, 20)
GRID = (18, 24, 45)
PANEL = (12, 17, 35)

SAVE_FILE = "neon_revenge_save.json"

# Music folder next to the game
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_FOLDER = os.path.join(BASE_DIR, "Music")
SUPPORTED_MUSIC = (".mp3", ".ogg", ".wav")

os.makedirs(MUSIC_FOLDER, exist_ok=True)

def scan_music_folder():
    try:
        return sorted(
            [
                f for f in os.listdir(MUSIC_FOLDER)
                if f.lower().endswith(SUPPORTED_MUSIC)
            ],
            key=str.lower
        )
    except Exception:
        return []

MUSIC_FILES = scan_music_folder()
MUSIC_NAMES = [os.path.splitext(f)[0] for f in MUSIC_FILES]


# =========================================================
# MUSIC
# =========================================================

music_index = 0
music_volume = 0.45
music_enabled = True


def music_path():
    if not MUSIC_FILES:
        return None

    return os.path.join(
        MUSIC_FOLDER,
        MUSIC_FILES[music_index]
    )


def play_music():

    global music_enabled

    path = music_path()

    if not path or not os.path.exists(path):
        music_enabled = False
        return

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        music_enabled = True
    except Exception:
        music_enabled = False


def next_music():

    global music_index

    if not MUSIC_FILES:
        return

    music_index = (
        music_index + 1
    ) % len(MUSIC_FILES)

    play_music()


def previous_music():

    global music_index

    if not MUSIC_FILES:
        return

    music_index -= 1

    if music_index < 0:
        music_index = len(MUSIC_FILES) - 1

    play_music()


def toggle_music():

    global music_enabled

    try:

        if music_enabled:

            pygame.mixer.music.pause()
            music_enabled = False

        else:

            pygame.mixer.music.unpause()
            music_enabled = True

    except:
        pass


try:

    pygame.mixer.init()
    play_music()

except:
    pass


# =========================================================
# SAVE
# =========================================================

DEFAULT_SAVE = {

    "coins": 0,
    "best_score": 0,

    "upgrade_damage": 0,
    "upgrade_speed": 0,
    "upgrade_hp": 0,
    "upgrade_fire": 0,
    "upgrade_dash": 0,
    "upgrade_crit": 0,
    "upgrade_multishot": 0,

    "difficulty": 1
}


def load_save():

    data = DEFAULT_SAVE.copy()

    if os.path.exists(SAVE_FILE):

        try:

            with open(
                SAVE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                old = json.load(f)

            for key in data:

                if key in old:
                    data[key] = old[key]

        except:
            pass

    return data


save_data = load_save()


def save_game():

    try:

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                save_data,
                f,
                ensure_ascii=False,
                indent=2
            )

    except:
        pass


# =========================================================
# DIFFICULTY
# =========================================================

DIFFICULTIES = [

    {
        "name": "EASY",
        "color": GREEN,

        "enemy_hp": 0.72,
        "enemy_speed": 0.78,
        "enemy_damage": 0.70,

        "boss_hp": 0.72,
        "boss_damage": 0.70,

        "spawn": 1.30,
        "reward": 1.35
    },

    {
        "name": "NORMAL",
        "color": YELLOW,

        "enemy_hp": 1.0,
        "enemy_speed": 1.0,
        "enemy_damage": 1.0,

        "boss_hp": 1.0,
        "boss_damage": 1.0,

        "spawn": 1.0,
        "reward": 1.0
    },

    {
        "name": "HARD",
        "color": RED,

        "enemy_hp": 1.35,
        "enemy_speed": 1.18,
        "enemy_damage": 1.30,

        "boss_hp": 1.35,
        "boss_damage": 1.30,

        "spawn": 0.72,
        "reward": 1.60
    }
]


def get_difficulty():

    index = int(
        save_data.get(
            "difficulty",
            1
        )
    )

    index = max(
        0,
        min(
            len(DIFFICULTIES) - 1,
            index
        )
    )

    return DIFFICULTIES[index]


# =========================================================
# HELPERS
# =========================================================

def clamp_value(v, a, b):

    return max(
        a,
        min(b, v)
    )


def draw_text(
    text,
    font,
    color,
    x,
    y,
    center=False
):

    img = font.render(
        str(text),
        True,
        color
    )

    rect = img.get_rect()

    if center:
        rect.center = (x, y)

    else:
        rect.topleft = (x, y)

    screen.blit(
        img,
        rect
    )


def glow_circle(
    x,
    y,
    radius,
    color
):

    for r, alpha in [

        (radius * 2.5, 20),
        (radius * 1.7, 35)

    ]:

        surf = pygame.Surface(
            (
                int(r * 2),
                int(r * 2)
            ),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surf,
            (*color, alpha),
            (
                int(r),
                int(r)
            ),
            int(r)
        )

        screen.blit(
            surf,
            (
                x - r,
                y - r
            )
        )

    pygame.draw.circle(
        screen,
        color,
        (
            int(x),
            int(y)
        ),
        int(radius)
    )


def angle_to(
    x1,
    y1,
    x2,
    y2
):

    return math.atan2(
        y2 - y1,
        x2 - x1
    )


def particles_add(
    x,
    y,
    color,
    amount=10
):

    for _ in range(amount):

        a = random.random() * math.tau
        s = random.uniform(
            1,
            6
        )

        particles.append({

            "x": x,
            "y": y,

            "vx": math.cos(a) * s,
            "vy": math.sin(a) * s,

            "life": random.randint(
                20,
                45
            ),

            "color": color,

            "size": random.randint(
                2,
                5
            )
        })


# =========================================================
# COMPLETE RESET - P
# =========================================================

def FULL_RESET():

    global save_data
    global music_index

    save_data = DEFAULT_SAVE.copy()

    music_index = 0

    save_game()

    reset_run()

    play_music()

    print(
        "NEON REVENGE RESET COMPLETE"
    )


# =========================================================
# PROJECTILE
# =========================================================

class Projectile:

    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        damage,
        color,
        enemy=False,
        life=100,
        radius=5
    ):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.damage = damage
        self.color = color
        self.enemy = enemy

        self.life = life
        self.radius = radius

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.life -= 1

    def draw(self):

        glow_circle(
            self.x,
            self.y,
            self.radius,
            self.color
        )


# =========================================================
# PLAYER
# =========================================================

class Player:

    def __init__(self):

        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.radius = 18

        # -------------------------------------------------
        # BASE VALUES
        # -------------------------------------------------

        self.max_hp = 100
        self.hp = 100

        self.damage = 18
        self.speed = 5.2

        self.fire_delay = 8

        self.dash_max = 70

        self.crit = 0.0

        self.multishot = 0

        # -------------------------------------------------
        # TIMERS
        # -------------------------------------------------

        self.fire_timer = 0
        self.dash_timer = 0
        self.dash_time = 0
        self.invincible = 0

        self.angle = 0

        self.coins = 0

        # -------------------------------------------------
        # APPLY SAVED UPGRADES
        # -------------------------------------------------

        self.refresh_stats(
            full_heal=True
        )

    # =====================================================
    # REFRESH ALL UPGRADE STATS
    # =====================================================

    def refresh_stats(
        self,
        full_heal=False
    ):

        old_max_hp = getattr(
            self,
            "max_hp",
            100
        )

        old_hp = getattr(
            self,
            "hp",
            100
        )

        # -------------------------------------------------
        # MAX HP
        # Level 0 = 100
        # Level 1 = 120
        # Level 2 = 140
        # -------------------------------------------------

        self.max_hp = (
            100 +
            save_data["upgrade_hp"] * 20
        )

        # -------------------------------------------------
        # DAMAGE
        # Level 0 = 18
        # Level 1 = 25
        # Level 2 = 32
        # -------------------------------------------------

        self.damage = (
            18 +
            save_data["upgrade_damage"] * 7
        )

        # -------------------------------------------------
        # SPEED
        # -------------------------------------------------

        self.speed = (
            5.2 +
            save_data["upgrade_speed"] * 0.55
        )

        # -------------------------------------------------
        # FIRE RATE
        # Lower delay = faster shooting
        # -------------------------------------------------

        self.fire_delay = max(
            2,
            8 -
            save_data["upgrade_fire"]
        )

        # -------------------------------------------------
        # DASH
        # Lower cooldown = faster dash
        # -------------------------------------------------

        self.dash_max = max(
            20,
            70 -
            save_data["upgrade_dash"] * 7
        )

        # -------------------------------------------------
        # CRITICAL
        # -------------------------------------------------

        self.crit = min(
            0.60,
            save_data["upgrade_crit"] * 0.06
        )

        # -------------------------------------------------
        # MULTI SHOT
        #
        # 0 = 1 bullet
        # 1 = 3 bullets
        # 2 = 5 bullets
        # -------------------------------------------------

        self.multishot = min(
            2,
            save_data["upgrade_multishot"]
        )

        # -------------------------------------------------
        # HP UPDATE
        # -------------------------------------------------

        if full_heal:

            self.hp = self.max_hp

        else:

            hp_difference = (
                self.max_hp -
                old_max_hp
            )

            self.hp = old_hp + hp_difference

            self.hp = min(
                self.hp,
                self.max_hp
            )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        keys = pygame.key.get_pressed()

        keyboard_dx = (
            keys[pygame.K_d] -
            keys[pygame.K_a]
        )

        keyboard_dy = (
            keys[pygame.K_s] -
            keys[pygame.K_w]
        )

        # Keyboard controls remain available on PC.
        if keyboard_dx or keyboard_dy:
            dx = keyboard_dx
            dy = keyboard_dy
        else:
            # On mobile, use the virtual joystick.
            dx, dy = touch_move

        if dx or dy:

            length = math.hypot(
                dx,
                dy
            )

            if length > 0:
                dx /= length
                dy /= length

                speed = self.speed

                if self.dash_time > 0:
                    speed = 15

                # Joystick strength controls walking speed.
                if not (keyboard_dx or keyboard_dy):
                    strength = min(1.0, length)
                    self.x += dx * speed * strength
                    self.y += dy * speed * strength
                else:
                    self.x += dx * speed
                    self.y += dy * speed

        self.x = clamp_value(
            self.x,
            30,
            WIDTH - 30
        )

        self.y = clamp_value(
            self.y,
            80,
            HEIGHT - 30
        )

        mx, my = pygame.mouse.get_pos()

        # Keep mouse aiming on PC. On mobile, aim toward the current boss.
        if boss is not None and touch_joystick_active:
            self.angle = angle_to(
                self.x,
                self.y,
                boss.x,
                boss.y
            )
        else:
            self.angle = angle_to(
                self.x,
                self.y,
                mx,
                my
            )

        self.fire_timer = max(
            0,
            self.fire_timer - 1
        )

        self.dash_timer = max(
            0,
            self.dash_timer - 1
        )

        self.dash_time = max(
            0,
            self.dash_time - 1
        )

        self.invincible = max(
            0,
            self.invincible - 1
        )

    # =====================================================
    # SHOOT
    # =====================================================

    def shoot(self):

        if self.fire_timer > 0:
            return []

        self.fire_timer = self.fire_delay

        result = []

        # -------------------------------------------------
        # REAL MULTI SHOT
        #
        # 0 -> 1
        # 1 -> 3
        # 2 -> 5
        # -------------------------------------------------

        bullet_count = (
            1 +
            self.multishot * 2
        )

        # Wider spread so bullets are clearly separated

        if bullet_count == 1:

            spreads = [0.0]

        elif bullet_count == 3:

            spreads = [
                -0.24,
                0.0,
                0.24
            ]

        else:

            spreads = [
                -0.42,
                -0.21,
                0.0,
                0.21,
                0.42
            ]

        for spread in spreads:

            a = self.angle + spread

            damage = self.damage

            # Critical hit

            if random.random() < self.crit:

                damage *= 2

            result.append(
                Projectile(

                    self.x,
                    self.y,

                    math.cos(a) * 13,
                    math.sin(a) * 13,

                    damage,

                    YELLOW,

                    False,

                    100,

                    5
                )
            )

        return result

    # =====================================================
    # DASH
    # =====================================================

    def dash(self):

        if self.dash_timer <= 0:

            self.dash_timer = self.dash_max

            self.dash_time = 8

            self.invincible = 14

    # =====================================================
    # TAKE DAMAGE
    # =====================================================

    def damage_player(self, amount):

        if self.invincible > 0:
            return

        self.hp -= amount

        self.invincible = 15

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        if (
            self.invincible > 0
            and
            (self.invincible // 2) % 2 == 0
        ):

            return

        glow_circle(
            self.x,
            self.y,
            self.radius,
            CYAN
        )

        gx = (
            self.x +
            math.cos(self.angle) * 30
        )

        gy = (
            self.y +
            math.sin(self.angle) * 30
        )

        pygame.draw.line(
            screen,
            WHITE,
            (
                self.x,
                self.y
            ),
            (
                gx,
                gy
            ),
            6
        )


# =========================================================
# ENEMY
# =========================================================

class Enemy:

    def __init__(self, kind):

        difficulty = get_difficulty()

        side = random.choice([
            "top",
            "bottom",
            "left",
            "right"
        ])

        if side == "top":

            self.x = random.randint(
                30,
                WIDTH - 30
            )

            self.y = -30

        elif side == "bottom":

            self.x = random.randint(
                30,
                WIDTH - 30
            )

            self.y = HEIGHT + 30

        elif side == "left":

            self.x = -30

            self.y = random.randint(
                80,
                HEIGHT - 30
            )

        else:

            self.x = WIDTH + 30

            self.y = random.randint(
                80,
                HEIGHT - 30
            )

        stats = {

            "normal": (
                55,
                1.8,
                15,
                18,
                RED,
                14
            ),

            "fast": (
                30,
                3.2,
                10,
                13,
                PINK,
                18
            ),

            "tank": (
                110,
                1.25,
                22,
                25,
                PURPLE,
                28
            ),

            "shooter": (
                45,
                1.1,
                8,
                17,
                ORANGE,
                22
            ),

            "exploder": (
                70,
                2.1,
                30,
                19,
                YELLOW,
                30
            )
        }

        (
            hp,
            speed,
            damage,
            radius,
            color,
            coins
        ) = stats[kind]

        self.hp = int(
            hp *
            difficulty["enemy_hp"]
        )

        self.speed = (
            speed *
            difficulty["enemy_speed"]
        )

        self.damage = int(
            damage *
            difficulty["enemy_damage"]
        )

        self.radius = radius

        self.color = color

        self.coins = int(
            coins *
            difficulty["reward"]
        )

        self.kind = kind

        self.max_hp = self.hp

        self.timer = random.randint(
            40,
            100
        )

    def update(self):

        dx = player.x - self.x
        dy = player.y - self.y

        dist = math.hypot(
            dx,
            dy
        )

        if dist > 0:

            nx = dx / dist
            ny = dy / dist

            if self.kind == "shooter":

                if dist > 300:

                    self.x += (
                        nx *
                        self.speed
                    )

                    self.y += (
                        ny *
                        self.speed
                    )

                elif dist < 220:

                    self.x -= (
                        nx *
                        self.speed
                    )

                    self.y -= (
                        ny *
                        self.speed
                    )

            else:

                self.x += (
                    nx *
                    self.speed
                )

                self.y += (
                    ny *
                    self.speed
                )

        self.timer -= 1

        if (
            self.kind == "shooter"
            and
            self.timer <= 0
        ):

            self.timer = 115

            a = angle_to(
                self.x,
                self.y,
                player.x,
                player.y
            )

            enemy_bullets.append(
                Projectile(

                    self.x,
                    self.y,

                    math.cos(a) * 5,
                    math.sin(a) * 5,

                    self.damage,

                    ORANGE,

                    True
                )
            )

        if (
            dist <
            self.radius +
            player.radius
            and
            self.timer <= 0
        ):

            player.damage_player(
                self.damage
            )

            self.timer = 45

    def draw(self):

        glow_circle(
            self.x,
            self.y,
            self.radius,
            self.color
        )


# =========================================================
# BOSSES
# =========================================================

BOSSES = [

    {
        "name": "NEON OVERLORD",
        "hp": 1300,
        "color": PURPLE,
        "reward": 300,
        "radius": 55
    },

    {
        "name": "CYBER TITAN",
        "hp": 2500,
        "color": RED,
        "reward": 500,
        "radius": 65
    },

    {
        "name": "THE NEON KING",
        "hp": 4500,
        "color": CYAN,
        "reward": 750,
        "radius": 72
    },

    {
        "name": "VOID REAPER",
        "hp": 6500,
        "color": (110, 40, 255),
        "reward": 1100,
        "radius": 78
    },

    {
        "name": "NEON DESTROYER",
        "hp": 9000,
        "color": ORANGE,
        "reward": 1600,
        "radius": 85
    },

    {
        "name": "FINAL OMEGA",
        "hp": 13000,
        "color": PINK,
        "reward": 2500,
        "radius": 95
    }
]


class Boss:

    def __init__(self, index):

        data = BOSSES[index]

        difficulty = get_difficulty()

        self.index = index

        self.name = data["name"]

        self.max_hp = int(
            data["hp"] *
            difficulty["boss_hp"]
        )

        self.hp = self.max_hp

        self.color = data["color"]

        self.reward = int(
            data["reward"] *
            difficulty["reward"]
        )

        self.radius = data["radius"]

        self.x = WIDTH / 2
        self.y = 130

        self.speed = (
            1.25 +
            index * 0.14
        ) * difficulty["enemy_speed"]

        self.attack_timer = 55

        self.special_timer = 170

    def update(self):

        difficulty = get_difficulty()

        dx = player.x - self.x
        dy = player.y - self.y

        dist = math.hypot(
            dx,
            dy
        )

        if dist > 250:

            self.x += (
                dx /
                dist *
                self.speed
            )

            self.y += (
                dy /
                dist *
                self.speed
            )

        self.attack_timer -= 1

        self.special_timer -= 1

        # -------------------------------------------------
        # CIRCLE ATTACK
        # -------------------------------------------------

        if self.attack_timer <= 0:

            self.attack_timer = max(
                32,
                70 -
                self.index * 4
            )

            count = (
                10 +
                self.index
            )

            for i in range(count):

                a = (
                    i *
                    math.tau /
                    count
                )

                speed = (
                    3.6 +
                    self.index * 0.25
                )

                damage = int(
                    (
                        7 +
                        self.index * 2
                    ) *
                    difficulty["boss_damage"]
                )

                enemy_bullets.append(
                    Projectile(

                        self.x,
                        self.y,

                        math.cos(a) * speed,
                        math.sin(a) * speed,

                        damage,

                        self.color,

                        True,

                        140,

                        5
                    )
                )

        # -------------------------------------------------
        # TARGETED ATTACK
        # -------------------------------------------------

        if self.special_timer <= 0:

            self.special_timer = max(
                95,
                190 -
                self.index * 10
            )

            base = angle_to(
                self.x,
                self.y,
                player.x,
                player.y
            )

            count = 2 + self.index

            for i in range(count):

                middle = (
                    count - 1
                ) / 2

                a = (
                    base +
                    (
                        i -
                        middle
                    ) * 0.13
                )

                damage = int(
                    (
                        12 +
                        self.index * 3
                    ) *
                    difficulty["boss_damage"]
                )

                enemy_bullets.append(
                    Projectile(

                        self.x,
                        self.y,

                        math.cos(a) * 5.5,
                        math.sin(a) * 5.5,

                        damage,

                        RED,

                        True,

                        160,

                        6
                    )
                )

        # -------------------------------------------------
        # SUMMON
        # -------------------------------------------------

        if (
            self.special_timer == 105
            and
            len(enemies) < 10
        ):

            amount = (
                1 +
                self.index // 2
            )

            for _ in range(amount):

                enemies.append(
                    Enemy(
                        random.choice([
                            "normal",
                            "fast",
                            "shooter",
                            "tank"
                        ])
                    )
                )

    def draw(self):

        glow_circle(
            self.x,
            self.y,
            self.radius,
            self.color
        )

        pygame.draw.circle(
            screen,
            RED,
            (
                int(self.x),
                int(self.y)
            ),
            18
        )

        width = 720

        x = (
            WIDTH -
            width
        ) / 2

        pygame.draw.rect(
            screen,
            (50, 20, 30),
            (
                x,
                20,
                width,
                22
            )
        )

        pygame.draw.rect(
            screen,
            RED,
            (
                x,
                20,
                width *
                max(
                    self.hp,
                    0
                ) /
                self.max_hp,
                22
            )
        )

        draw_text(
            self.name,
            FONT,
            WHITE,
            WIDTH // 2,
            65,
            True
        )


# =========================================================
# UPGRADES
# =========================================================

UPGRADES = [

    (
        "DAMAGE",
        "upgrade_damage",
        50
    ),

    (
        "SPEED",
        "upgrade_speed",
        65
    ),

    (
        "MAX HP",
        "upgrade_hp",
        60
    ),

    (
        "FIRE RATE",
        "upgrade_fire",
        90
    ),

    (
        "DASH",
        "upgrade_dash",
        85
    ),

    (
        "CRITICAL",
        "upgrade_crit",
        110
    ),

    (
        "MULTI SHOT",
        "upgrade_multishot",
        220
    )
]


def upgrade_cost(i):

    name, key, base = UPGRADES[i]

    return (
        base +
        save_data[key] *
        int(base * 0.65)
    )


def buy_upgrade(i):

    global player

    if i < 0 or i >= len(UPGRADES):
        return

    name, key, base = UPGRADES[i]

    # -----------------------------------------------------
    # MULTI SHOT MAX LEVEL = 2
    # -----------------------------------------------------

    if (
        key == "upgrade_multishot"
        and
        save_data[key] >= 2
    ):

        return

    cost = upgrade_cost(i)

    if save_data["coins"] < cost:
        return

    # -----------------------------------------------------
    # PAY
    # -----------------------------------------------------

    save_data["coins"] -= cost

    # -----------------------------------------------------
    # LEVEL UP
    # -----------------------------------------------------

    save_data[key] += 1

    # -----------------------------------------------------
    # APPLY IMMEDIATELY
    # -----------------------------------------------------

    player.refresh_stats()

    # -----------------------------------------------------
    # HP UPGRADE:
    # Fill HP completely after buying Max HP
    # -----------------------------------------------------

    if key == "upgrade_hp":

        player.hp = player.max_hp

    save_game()

    print(
        f"UPGRADE: {name} -> "
        f"LV {save_data[key]}"
    )


# =========================================================
# LOBBY
# =========================================================

def draw_lobby():

    screen.fill(DARK)

    draw_text(
        "NEON LOBBY",
        HUGE,
        CYAN,
        WIDTH // 2,
        50,
        True
    )

    draw_text(
        "MAHDI STUDIO",
        BIG,
        PURPLE,
        WIDTH // 2,
        105,
        True
    )

    draw_text(
        f"COINS: {save_data['coins']}",
        BIG,
        YELLOW,
        WIDTH // 2,
        145,
        True
    )

    # -----------------------------------------------------
    # BOSS PANEL
    # -----------------------------------------------------

    pygame.draw.rect(
        screen,
        PANEL,
        (
            55,
            180,
            470,
            205
        ),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        CYAN,
        (
            55,
            180,
            470,
            205
        ),
        2,
        border_radius=12
    )

    if current_boss < len(BOSSES):

        data = BOSSES[current_boss]

        draw_text(
            f"BOSS {current_boss + 1} / 6",
            FONT,
            PINK,
            290,
            205,
            True
        )

        draw_text(
            data["name"],
            BIG,
            data["color"],
            290,
            250,
            True
        )

        diff = get_difficulty()

        boss_hp = int(
            data["hp"] *
            diff["boss_hp"]
        )

        draw_text(
            f"HP: {boss_hp}",
            SMALL,
            WHITE,
            290,
            300,
            True
        )

        draw_text(
            (
                f"REWARD: "
                f"{int(data['reward'] * diff['reward'])} COINS"
            ),
            SMALL,
            YELLOW,
            290,
            330,
            True
        )

        draw_text(
            "ENTER = FIGHT",
            FONT,
            GREEN,
            290,
            360,
            True
        )

    else:

        draw_text(
            "ALL BOSSES DEFEATED!",
            BIG,
            GREEN,
            290,
            270,
            True
        )

    # -----------------------------------------------------
    # UPGRADES
    # -----------------------------------------------------

    draw_text(
        "UPGRADES",
        FONT,
        CYAN,
        570,
        165
    )

    for i, (
        name,
        key,
        base
    ) in enumerate(UPGRADES):

        col = i % 2
        row = i // 2

        x = (
            570 +
            col * 250
        )

        y = (
            200 +
            row * 42
        )

        level = save_data[key]

        if (
            key == "upgrade_multishot"
            and
            level >= 2
        ):

            price = "MAX"

        else:

            price = (
                f"{upgrade_cost(i)} C"
            )

        draw_text(
            f"{i + 1}. {name}",
            SMALL,
            WHITE,
            x,
            y
        )

        draw_text(
            f"LV.{level} [{price}]",
            SMALL,
            YELLOW,
            x,
            y + 19
        )

    # -----------------------------------------------------
    # PLAYER BUILD PANEL
    # -----------------------------------------------------

    panel_x = max(835, WIDTH - 340)
    panel_y = 145
    panel_w = 285
    panel_h = 505

    pygame.draw.rect(
        screen,
        PANEL,
        (panel_x, panel_y, panel_w, panel_h),
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (panel_x, panel_y, panel_w, panel_h),
        2,
        border_radius=14
    )

    draw_text(
        "PLAYER BUILD",
        FONT,
        GREEN,
        panel_x + panel_w // 2,
        panel_y + 28,
        True
    )

    draw_text(
        "UPGRADE TABLE",
        SMALL,
        WHITE,
        panel_x + panel_w // 2,
        panel_y + 54,
        True
    )

    # Every upgrade gets its own row in the table.
    # The rows below include DASH and MULTI SHOT too.

    def draw_level_dots(label, level, y, value, accent):
        draw_text(
            label,
            SMALL,
            WHITE,
            panel_x + 20,
            y
        )

        draw_text(
            f"LV.{level}",
            SMALL,
            accent,
            panel_x + panel_w - 55,
            y
        )

        dot_start_x = panel_x + 22
        dot_y = y + 24

        # Five visual level slots: filled = unlocked,
        # hollow = locked.
        for dot in range(5):
            cx = dot_start_x + dot * 42
            if dot < min(level, 5):
                pygame.draw.circle(
                    screen,
                    accent,
                    (cx, dot_y),
                    7
                )
            else:
                pygame.draw.circle(
                    screen,
                    accent,
                    (cx, dot_y),
                    7,
                    2
                )

        draw_text(
            value,
            SMALL,
            accent,
            panel_x + panel_w - 58,
            dot_y,
            True
        )

    # All 7 upgrades now have their own level dots.
    draw_level_dots(
        "DAMAGE",
        save_data["upgrade_damage"],
        panel_y + 82,
        f"{player.damage}",
        PINK
    )

    draw_level_dots(
        "MAX HP",
        save_data["upgrade_hp"],
        panel_y + 137,
        f"{player.max_hp}",
        CYAN
    )

    draw_level_dots(
        "SPEED",
        save_data["upgrade_speed"],
        panel_y + 192,
        f"{player.speed:.1f}",
        GREEN
    )

    draw_level_dots(
        "FIRE RATE",
        save_data["upgrade_fire"],
        panel_y + 247,
        f"{player.fire_delay}",
        YELLOW
    )

    draw_level_dots(
        "DASH",
        save_data["upgrade_dash"],
        panel_y + 302,
        f"{player.dash_max}",
        ORANGE
    )

    draw_level_dots(
        "CRITICAL",
        save_data["upgrade_crit"],
        panel_y + 357,
        f"{int(player.crit * 100)}%",
        PURPLE
    )

    draw_level_dots(
        "MULTI SHOT",
        save_data["upgrade_multishot"],
        panel_y + 412,
        f"{1 + player.multishot * 2}B",
        CYAN
    )

    # -----------------------------------------------------
    # MUSIC
    # -----------------------------------------------------

    # -----------------------------------------------------

    pygame.draw.rect(
        screen,
        PANEL,
        (
            55,
            420,
            470,
            170
        ),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        PURPLE,
        (
            55,
            420,
            470,
            170
        ),
        2,
        border_radius=12
    )

    draw_text(
        "MUSIC",
        FONT,
        PURPLE,
        75,
        415
    )

    if MUSIC_FILES:
        draw_text(
            f"{music_index + 1}. {MUSIC_NAMES[music_index]}",
            SMALL,
            WHITE,
            75,
            455
        )
    else:
        draw_text(
            "No music found - add songs to Music/",
            SMALL,
            RED,
            75,
            455
        )

    draw_text(
        "J = Previous",
        SMALL,
        CYAN,
        75,
        490
    )

    draw_text(
        "K = Play / Pause",
        SMALL,
        CYAN,
        75,
        515
    )

    draw_text(
        "L = Next",
        SMALL,
        CYAN,
        75,
        540
    )

    status = (
        "PLAYING"
        if music_enabled
        else
        "PAUSED"
    )

    draw_text(
        status,
        SMALL,
        (
            GREEN
            if music_enabled
            else RED
        ),
        370,
        515
    )

    # -----------------------------------------------------
    # CONTROLS
    # -----------------------------------------------------

    draw_text(
        "1-7 BUY UPGRADE",
        SMALL,
        CYAN,
        WIDTH // 2,
        610,
        True
    )

    draw_text(
        "S = SETTINGS",
        SMALL,
        ORANGE,
        WIDTH // 2,
        635,
        True
    )

    draw_text(
        "P = FULL RESET",
        SMALL,
        RED,
        WIDTH // 2,
        660,
        True
    )


# =========================================================
# SETTINGS
# =========================================================

def draw_settings():

    screen.fill(DARK)

    draw_text(
        "SETTINGS",
        HUGE,
        CYAN,
        WIDTH // 2,
        80,
        True
    )

    draw_text(
        "DIFFICULTY",
        BIG,
        WHITE,
        WIDTH // 2,
        190,
        True
    )

    diff = get_difficulty()

    draw_text(
        diff["name"],
        HUGE,
        diff["color"],
        WIDTH // 2,
        285,
        True
    )

    draw_text(
        "LEFT / RIGHT = CHANGE",
        FONT,
        WHITE,
        WIDTH // 2,
        365,
        True
    )

    draw_text(
        "ENTER = SAVE & LOBBY",
        FONT,
        GREEN,
        WIDTH // 2,
        400,
        True
    )

    draw_text(
        "ESC = BACK",
        FONT,
        YELLOW,
        WIDTH // 2,
        435,
        True
    )

    if save_data["difficulty"] == 0:

        draw_text(
            "Enemies and bosses are weaker.",
            SMALL,
            GREEN,
            WIDTH // 2,
            490,
            True
        )

    elif save_data["difficulty"] == 1:

        draw_text(
            "Standard NEON REVENGE difficulty.",
            SMALL,
            YELLOW,
            WIDTH // 2,
            490,
            True
        )

    else:

        draw_text(
            "Enemies and bosses are stronger.",
            SMALL,
            RED,
            WIDTH // 2,
            490,
            True
        )

    draw_text(
        "P = FULL RESET",
        SMALL,
        RED,
        WIDTH // 2,
        600,
        True
    )


# =========================================================
# RESET RUN
# =========================================================

def reset_run():

    global player
    global bullets
    global enemy_bullets
    global enemies
    global particles
    global boss
    global score
    global current_boss
    global victory_boss_number
    global game_state
    global spawn_timer

    player = Player()

    bullets = []
    enemy_bullets = []
    enemies = []
    particles = []

    boss = None

    score = 0

    current_boss = 0

    victory_boss_number = 0

    spawn_timer = 0

    game_state = "lobby"


# =========================================================
# START BOSS
# =========================================================

def start_boss():

    global boss
    global game_state
    global enemies
    global enemy_bullets

    if current_boss >= len(BOSSES):
        return

    # -----------------------------------------------------
    # IMPORTANT:
    # Sync all upgrades before entering battle
    # -----------------------------------------------------

    player.refresh_stats(
        full_heal=True
    )

    enemies.clear()
    enemy_bullets.clear()
    bullets.clear()

    player.hp = player.max_hp

    player.x = WIDTH // 2
    player.y = HEIGHT // 2

    boss = Boss(
        current_boss
    )

    game_state = "boss"


# =========================================================
# INITIAL
# =========================================================

player = Player()

bullets = []
enemy_bullets = []
enemies = []
particles = []

boss = None

score = 0

current_boss = 0

victory_boss_number = 0

spawn_timer = 0

# =========================================================
# MOBILE TOUCH CONTROLS
# =========================================================
touch_joystick_active = False
touch_joystick_id = None
touch_joystick_pos = (0, 0)
touch_move = (0.0, 0.0)
touch_fire = False
touch_dash = False

JOYSTICK_CENTER = (125, HEIGHT - 125)
JOYSTICK_RADIUS = 75
FIRE_BUTTON_CENTER = (WIDTH - 125, HEIGHT - 135)
FIRE_BUTTON_RADIUS = 62
DASH_BUTTON_CENTER = (WIDTH - 255, HEIGHT - 95)
DASH_BUTTON_RADIUS = 45

def point_in_circle(pos, center, radius):
    return math.hypot(pos[0] - center[0], pos[1] - center[1]) <= radius

def update_touch_joystick(pos):
    global touch_move, touch_joystick_pos

    cx, cy = JOYSTICK_CENTER
    dx = pos[0] - cx
    dy = pos[1] - cy
    dist = math.hypot(dx, dy)

    if dist > JOYSTICK_RADIUS:
        dx = dx / dist * JOYSTICK_RADIUS
        dy = dy / dist * JOYSTICK_RADIUS
        dist = JOYSTICK_RADIUS

    touch_joystick_pos = (cx + dx, cy + dy)

    if JOYSTICK_RADIUS > 0:
        touch_move = (dx / JOYSTICK_RADIUS, dy / JOYSTICK_RADIUS)

def reset_touch_controls():
    global touch_joystick_active, touch_joystick_id
    global touch_joystick_pos, touch_move, touch_fire, touch_dash

    touch_joystick_active = False
    touch_joystick_id = None
    touch_joystick_pos = JOYSTICK_CENTER
    touch_move = (0.0, 0.0)
    touch_fire = False
    touch_dash = False

# Start with the joystick knob centered.
touch_joystick_pos = JOYSTICK_CENTER

game_state = "lobby"

running = True


# =========================================================
# MAIN LOOP
# =========================================================

while running:

    clock.tick(FPS)

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            save_game()

            running = False

        # =================================================
        # MOBILE TOUCH EVENTS
        # =================================================

        if event.type == pygame.FINGERDOWN:

            tx = int(event.x * WIDTH)
            ty = int(event.y * HEIGHT)

            if game_state == "boss":

                if point_in_circle((tx, ty), JOYSTICK_CENTER, JOYSTICK_RADIUS * 1.35):
                    touch_joystick_active = True
                    touch_joystick_id = event.finger_id
                    update_touch_joystick((tx, ty))

                elif point_in_circle((tx, ty), FIRE_BUTTON_CENTER, FIRE_BUTTON_RADIUS):
                    touch_fire = True

                elif point_in_circle((tx, ty), DASH_BUTTON_CENTER, DASH_BUTTON_RADIUS):
                    touch_dash = True
                    player.dash()

        elif event.type == pygame.FINGERMOTION:

            if event.finger_id == touch_joystick_id:
                update_touch_joystick((int(event.x * WIDTH), int(event.y * HEIGHT)))

        elif event.type == pygame.FINGERUP:

            if event.finger_id == touch_joystick_id:
                touch_joystick_active = False
                touch_joystick_id = None
                touch_move = (0.0, 0.0)
                touch_joystick_pos = JOYSTICK_CENTER

            tx = int(event.x * WIDTH)
            ty = int(event.y * HEIGHT)

            if point_in_circle((tx, ty), FIRE_BUTTON_CENTER, FIRE_BUTTON_RADIUS):
                touch_fire = False

            if point_in_circle((tx, ty), DASH_BUTTON_CENTER, DASH_BUTTON_RADIUS):
                touch_dash = False

        if event.type == pygame.KEYDOWN:

            # -------------------------------------------------
            # FULL RESET
            # -------------------------------------------------

            if event.key == pygame.K_p:

                FULL_RESET()

                continue

            # -------------------------------------------------
            # MUSIC
            # -------------------------------------------------

            if event.key == pygame.K_j:

                previous_music()

            elif event.key == pygame.K_k:

                toggle_music()

            elif event.key == pygame.K_l:

                next_music()

            # =================================================
            # LOBBY
            # =================================================

            elif game_state == "lobby":

                if (
                    pygame.K_1
                    <= event.key
                    <= pygame.K_7
                ):

                    buy_upgrade(
                        event.key -
                        pygame.K_1
                    )

                elif event.key == pygame.K_RETURN:

                    start_boss()

                elif event.key == pygame.K_s:

                    game_state = "settings"

            # =================================================
            # SETTINGS
            # =================================================

            elif game_state == "settings":

                if event.key == pygame.K_LEFT:

                    save_data["difficulty"] -= 1

                    if save_data["difficulty"] < 0:

                        save_data["difficulty"] = 2

                    save_game()

                elif event.key == pygame.K_RIGHT:

                    save_data["difficulty"] += 1

                    if save_data["difficulty"] > 2:

                        save_data["difficulty"] = 0

                    save_game()

                elif event.key == pygame.K_RETURN:

                    save_game()

                    game_state = "lobby"

                elif event.key == pygame.K_ESCAPE:

                    game_state = "lobby"

            # =================================================
            # BOSS
            # =================================================

            elif game_state == "boss":

                if event.key == pygame.K_SPACE:

                    bullets.extend(
                        player.shoot()
                    )

                elif event.key == pygame.K_LSHIFT:

                    player.dash()

                elif event.key == pygame.K_ESCAPE:

                    boss = None

                    enemy_bullets.clear()

                    enemies.clear()

                    bullets.clear()

                    game_state = "lobby"

            # =================================================
            # VICTORY
            # =================================================

            elif game_state == "victory":

                if event.key == pygame.K_RETURN:

                    if current_boss >= len(BOSSES):

                        FULL_RESET()

                    else:

                        game_state = "lobby"

    # =====================================================
    # BOSS UPDATE
    # =====================================================

    if game_state == "boss":

        player.update()

        # -------------------------------------------------
        # Mouse shooting
        # -------------------------------------------------

        mouse = pygame.mouse.get_pressed()

        if mouse[0] or touch_fire:

            bullets.extend(
                player.shoot()
            )

        if touch_dash:
            player.dash()

        # -------------------------------------------------
        # Boss
        # -------------------------------------------------

        if boss:

            boss.update()

        # =================================================
        # PLAYER BULLETS
        # =================================================

        for bullet in bullets[:]:

            bullet.update()

            if (
                bullet.life <= 0
                or
                bullet.x < -100
                or
                bullet.x > WIDTH + 100
                or
                bullet.y < -100
                or
                bullet.y > HEIGHT + 100
            ):

                if bullet in bullets:

                    bullets.remove(
                        bullet
                    )

                continue

            # -------------------------------------------------
            # Boss collision
            # -------------------------------------------------

            if boss:

                distance = math.hypot(
                    bullet.x - boss.x,
                    bullet.y - boss.y
                )

                if distance < boss.radius:

                    boss.hp -= bullet.damage

                    particles_add(
                        bullet.x,
                        bullet.y,
                        boss.color,
                        4
                    )

                    if bullet in bullets:

                        bullets.remove(
                            bullet
                        )

                    if boss.hp <= 0:

                        # =================================
                        # BOSS DEFEATED
                        # =================================

                        save_data["coins"] += (
                            player.coins
                        )

                        save_data["coins"] += (
                            boss.reward
                        )

                        player.coins = 0

                        score += (
                            2500 +
                            current_boss * 1000
                        )

                        victory_boss_number = current_boss + 1

                        save_data["best_score"] = max(
                            save_data["best_score"],
                            score
                        )

                        particles_add(
                            boss.x,
                            boss.y,
                            boss.color,
                            180
                        )

                        boss = None

                        current_boss += 1

                        save_game()

                        # Show VICTORY after EVERY boss.
                        # The victory screen tells the player which boss
                        # number was just defeated, then Enter continues
                        # to the next boss through the lobby.
                        game_state = "victory"

                    continue

        # =================================================
        # ENEMY SPAWN
        # =================================================

        difficulty = get_difficulty()

        spawn_timer -= 1

        base_max = (
            2 +
            current_boss
        )

        max_enemies = int(
            base_max /
            difficulty["spawn"]
        )

        if (
            spawn_timer <= 0
            and
            len(enemies) < max_enemies
        ):

            kinds = [
                "normal",
                "fast"
            ]

            if current_boss >= 1:

                kinds.append(
                    "shooter"
                )

            if current_boss >= 2:

                kinds.append(
                    "tank"
                )

            if current_boss >= 3:

                kinds.append(
                    "exploder"
                )

            enemies.append(
                Enemy(
                    random.choice(kinds)
                )
            )

            spawn_timer = int(
                85 *
                difficulty["spawn"]
            )

        # =================================================
        # ENEMIES
        # =================================================

        for enemy in enemies[:]:

            enemy.update()

            if enemy.hp <= 0:

                if enemy in enemies:

                    enemies.remove(
                        enemy
                    )

                continue

            for bullet in bullets[:]:

                if math.hypot(
                    bullet.x - enemy.x,
                    bullet.y - enemy.y
                ) < enemy.radius:

                    enemy.hp -= bullet.damage

                    if bullet in bullets:

                        bullets.remove(
                            bullet
                        )

                    if enemy.hp <= 0:

                        player.coins += (
                            enemy.coins
                        )

                        score += (
                            enemy.coins * 5
                        )

                        particles_add(
                            enemy.x,
                            enemy.y,
                            enemy.color,
                            15
                        )

                        if enemy in enemies:

                            enemies.remove(
                                enemy
                            )

                    break

        # =================================================
        # ENEMY BULLETS
        # =================================================

        for bullet in enemy_bullets[:]:

            bullet.update()

            if bullet.life <= 0:

                if bullet in enemy_bullets:

                    enemy_bullets.remove(
                        bullet
                    )

                continue

            if math.hypot(
                bullet.x - player.x,
                bullet.y - player.y
            ) < (
                player.radius +
                bullet.radius
            ):

                player.damage_player(
                    bullet.damage
                )

                particles_add(
                    player.x,
                    player.y,
                    RED,
                    8
                )

                if bullet in enemy_bullets:

                    enemy_bullets.remove(
                        bullet
                    )

        # =================================================
        # PARTICLES
        # =================================================

        for p in particles[:]:

            p["x"] += p["vx"]
            p["y"] += p["vy"]

            p["vx"] *= 0.96
            p["vy"] *= 0.96

            p["life"] -= 1

            if p["life"] <= 0:

                particles.remove(
                    p
                )

        # =================================================
        # PLAYER DEAD
        # =================================================

        if player.hp <= 0:

            save_data["coins"] += (
                player.coins
            )

            player.coins = 0

            save_data["best_score"] = max(
                save_data["best_score"],
                score
            )

            save_game()

            boss = None

            enemies.clear()

            enemy_bullets.clear()

            bullets.clear()

            game_state = "lobby"

    # =====================================================
    # DRAW BACKGROUND
    # =====================================================

    screen.fill(DARK)

    for x in range(
        0,
        WIDTH,
        50
    ):

        pygame.draw.line(
            screen,
            GRID,
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(
        0,
        HEIGHT,
        50
    ):

        pygame.draw.line(
            screen,
            GRID,
            (0, y),
            (WIDTH, y)
        )

    # =====================================================
    # BOSS
    # =====================================================

    if game_state == "boss":

        pygame.draw.rect(
            screen,
            (10, 13, 28),
            (
                0,
                0,
                WIDTH,
                65
            )
        )

        pygame.draw.line(
            screen,
            CYAN,
            (
                0,
                64
            ),
            (
                WIDTH,
                64
            ),
            2
        )

        for enemy in enemies:

            enemy.draw()

        if boss:

            boss.draw()

        for bullet in bullets:

            bullet.draw()

        for bullet in enemy_bullets:

            bullet.draw()

        for p in particles:

            pygame.draw.circle(
                screen,
                p["color"],
                (
                    int(p["x"]),
                    int(p["y"])
                ),
                p["size"]
            )

        player.draw()

        # -------------------------------------------------
        # MOBILE TOUCH CONTROLS
        # -------------------------------------------------

        # Joystick
        pygame.draw.circle(
            screen,
            (25, 35, 60),
            JOYSTICK_CENTER,
            JOYSTICK_RADIUS
        )
        pygame.draw.circle(
            screen,
            CYAN,
            JOYSTICK_CENTER,
            JOYSTICK_RADIUS,
            3
        )
        pygame.draw.circle(
            screen,
            (30, 220, 255),
            (int(touch_joystick_pos[0]), int(touch_joystick_pos[1])),
            28
        )
        draw_text(
            "MOVE",
            SMALL,
            WHITE,
            JOYSTICK_CENTER[0],
            JOYSTICK_CENTER[1] - 8,
            True
        )

        # Fire button
        pygame.draw.circle(
            screen,
            (70, 20, 55),
            FIRE_BUTTON_CENTER,
            FIRE_BUTTON_RADIUS
        )
        pygame.draw.circle(
            screen, PINK, FIRE_BUTTON_CENTER, FIRE_BUTTON_RADIUS, 4
        )
        draw_text(
            "FIRE",
            SMALL,
            WHITE,
            FIRE_BUTTON_CENTER[0],
            FIRE_BUTTON_CENTER[1],
            True
        )

        # Dash button
        pygame.draw.circle(
            screen,
            (25, 45, 70),
            DASH_BUTTON_CENTER,
            DASH_BUTTON_RADIUS
        )
        pygame.draw.circle(
            screen, CYAN, DASH_BUTTON_CENTER, DASH_BUTTON_RADIUS, 3
        )
        draw_text(
            "DASH",
            SMALL,
            WHITE,
            DASH_BUTTON_CENTER[0],
            DASH_BUTTON_CENTER[1],
            True
        )

        # -------------------------------------------------
        # HP BAR
        # -------------------------------------------------

        pygame.draw.rect(
            screen,
            (50, 40, 50),
            (
                20,
                80,
                240,
                18
            )
        )

        hp_ratio = 0

        if player.max_hp > 0:

            hp_ratio = (
                max(
                    player.hp,
                    0
                ) /
                player.max_hp
            )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                20,
                80,
                int(
                    240 *
                    hp_ratio
                ),
                18
            )
        )

        draw_text(
            (
                f"HP "
                f"{max(0, int(player.hp))}/"
                f"{player.max_hp}"
            ),
            SMALL,
            WHITE,
            20,
            104
        )

        draw_text(
            f"BOSS {current_boss + 1}/6",
            FONT,
            PINK,
            300,
            20
        )

        draw_text(
            (
                f"COINS "
                f"{save_data['coins'] + player.coins}"
            ),
            FONT,
            YELLOW,
            500,
            20
        )

        draw_text(
            (
                f"DIFFICULTY: "
                f"{get_difficulty()['name']}"
            ),
            SMALL,
            get_difficulty()["color"],
            760,
            22
        )

        draw_text(
            "SHIFT DASH | SPACE / MOUSE SHOOT | ESC LOBBY",
            SMALL,
            WHITE,
            WIDTH // 2,
            HEIGHT - 25,
            True
        )

    # =====================================================
    # LOBBY
    # =====================================================

    elif game_state == "lobby":

        draw_lobby()

    # =====================================================
    # SETTINGS
    # =====================================================

    elif game_state == "settings":

        draw_settings()

    # =====================================================
    # VICTORY
    # =====================================================

    elif game_state == "victory":

        screen.fill(DARK)

        draw_text(
            "VICTORY",
            HUGE,
            CYAN,
            WIDTH // 2,
            150,
            True
        )

        draw_text(
            f"BOSS {victory_boss_number} DEFEATED",
            BIG,
            PINK,
            WIDTH // 2,
            250,
            True
        )

        if victory_boss_number >= len(BOSSES):

            draw_text(
                "DEMO COMPLETE",
                FONT,
                GREEN,
                WIDTH // 2,
                320,
                True
            )

        else:

            draw_text(
                f"BOSS {victory_boss_number} COMPLETE",
                FONT,
                GREEN,
                WIDTH // 2,
                320,
                True
            )

        draw_text(
            f"FINAL SCORE: {score}",
            FONT,
            YELLOW,
            WIDTH // 2,
            365,
            True
        )

        draw_text(
            (
                f"TOTAL COINS: "
                f"{save_data['coins']}"
            ),
            FONT,
            CYAN,
            WIDTH // 2,
            405,
            True
        )

        draw_text(
            (
                "PRESS ENTER TO CONTINUE"
                if victory_boss_number < len(BOSSES)
                else "PRESS ENTER TO RESET EVERYTHING"
            ),
            FONT,
            WHITE,
            WIDTH // 2,
            500,
            True
        )

        draw_text(
            "P = FULL RESET",
            SMALL,
            RED,
            WIDTH // 2,
            550,
            True
        )

    pygame.display.flip()


# =========================================================
# EXIT
# =========================================================

save_game()

try:

    pygame.mixer.music.stop()

except:
    pass

pygame.quit()
