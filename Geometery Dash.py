import math
import random
import tkinter as tk

# -------------------------------------------------------------------
# Game States Constants
# -------------------------------------------------------------------
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAMEOVER = "GAMEOVER"
STATE_WIN = "WIN"


# -------------------------------------------------------------------
# Base Hierarchy (Abstraction & Inheritance)
# -------------------------------------------------------------------
class GameObject:
    """Base abstract entity representing spatial objects on canvas."""

    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = None
        self.passed = False  # Track if player successfully passed this object

    def draw(self):
        """Must be overridden or handled by derived classes."""
        pass

    def update(self, scroll_speed):
        """Scroll object leftward to simulate forward player motion."""
        self.x -= scroll_speed
        self.draw()

    def destroy(self):
        if self.id:
            if isinstance(self.id, (tuple, list)):
                for item in self.id:
                    self.canvas.delete(item)
            else:
                self.canvas.delete(self.id)


# -------------------------------------------------------------------
# Polymorphic Game Entities
# -------------------------------------------------------------------
class Spike(GameObject):
    """Hazardous triangular spike obstacle."""

    def __init__(self, canvas, x, y, width, height, color="#FF4444"):
        super().__init__(canvas, x, y, width, height, color)

    def draw(self):
        p1 = (self.x, self.y + self.height)
        p2 = (self.x + self.width / 2, self.y)
        p3 = (self.x + self.width, self.y + self.height)

        if self.id is None:
            self.id = self.canvas.create_polygon(
                p1, p2, p3, fill=self.color, outline="#FF6666", width=2
            )
        else:
            self.canvas.coords(
                self.id, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
            )

    def is_colliding(self, player):
        """Bounding box overlap check with forgiveness tolerance."""
        tolerance = 5
        px, py, pw, ph = (
            player.x + tolerance,
            player.y + tolerance,
            player.width - (2 * tolerance),
            player.height - (2 * tolerance),
        )

        return (
            px < self.x + self.width
            and px + pw > self.x
            and py < self.y + self.height
            and py + ph > self.y
        )


class JumpPad(GameObject):
    """Interactive orb/pad that launches player high into the air."""

    def __init__(self, canvas, x, y, size=30):
        super().__init__(canvas, x, y, size, size / 3, color="#FFFF00")
        self.boost_power = -22
        self.activated = False

    def draw(self):
        if self.id is None:
            self.id = self.canvas.create_oval(
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height,
                fill=self.color,
                outline="#FFFFFF",
                width=2,
            )
        else:
            self.canvas.coords(
                self.id,
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height,
            )

    def check_trigger(self, player):
        """Boosts player velocity if touched."""
        collides = (
            player.x < self.x + self.width
            and player.x + player.width > self.x
            and player.y < self.y + self.height
            and player.y + player.height > self.y
        )

        if collides and not self.activated:
            player.vy = self.boost_power
            self.activated = True
            self.color = "#888800"  # Dim pad after use
            return True
        return False


class ScorePopup:
    """Floating '+10' text entity that drifts up and disappears."""

    def __init__(self, canvas, x, y, text="+10"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.lifetime = 20
        self.id = self.canvas.create_text(
            x,
            y,
            text=text,
            fill="#00FF88",
            font=("Impact", 16, "bold"),
            anchor="center",
        )

    def update(self):
        self.y -= 2.5  # Float upward
        self.lifetime -= 1
        self.canvas.coords(self.id, self.x, self.y)
        return self.lifetime <= 0

    def destroy(self):
        self.canvas.delete(self.id)


class Particle:
    """Visual dust / death explosion effect particle."""

    def __init__(self, canvas, x, y, vx, vy, color, size=4, lifetime=15):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.id = self.canvas.create_oval(
            x, y, x + size, y + size, fill=color, outline=""
        )

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.canvas.coords(
            self.id, self.x, self.y, self.x + self.size, self.y + self.size
        )
        return self.lifetime <= 0

    def destroy(self):
        self.canvas.delete(self.id)


# -------------------------------------------------------------------
# Player Class (Physics & Encapsulation)
# -------------------------------------------------------------------
class Player(GameObject):
    """Encapsulates Physics, Jump mechanics, and Polygon rotation rendering."""

    def __init__(self, canvas, x, y, size=36):
        super().__init__(canvas, x, y, size, size, color="#00FFCC")
        self.ground_y = y
        self.vy = 0
        self.gravity = 1.25
        self.jump_strength = -15.5
        self.is_grounded = True
        self.angle = 0  # Rotation degrees

    def jump(self):
        if self.is_grounded:
            self.vy = self.jump_strength
            self.is_grounded = False

    def update_physics(self):
        self.vy += self.gravity
        self.y += self.vy

        # Rotation during air time
        if not self.is_grounded:
            self.angle += 8.5
        else:
            self.angle = round(self.angle / 90) * 90

        # Ground collision
        if self.y >= self.ground_y:
            just_landed = not self.is_grounded
            self.y = self.ground_y
            self.vy = 0
            self.is_grounded = True
            self.draw()
            return just_landed

        self.draw()
        return False

    def draw(self):
        """Rotates corners around center point to create continuous turning effect."""
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        rad = math.radians(self.angle)

        half = self.width / 2
        corners = [(-half, -half), (half, -half), (half, half), (-half, half)]

        rotated_coords = []
        for rx, ry in corners:
            nx = rx * math.cos(rad) - ry * math.sin(rad)
            ny = rx * math.sin(rad) + ry * math.cos(rad)
            rotated_coords.append(cx + nx)
            rotated_coords.append(cy + ny)

        if self.id is None:
            self.id = self.canvas.create_polygon(
                rotated_coords, fill=self.color, outline="#FFFFFF", width=2
            )
        else:
            self.canvas.coords(self.id, *rotated_coords)


# -------------------------------------------------------------------
# Factory Pattern & Level Generator
# -------------------------------------------------------------------
class LevelFactory:
    """Handles dynamic generation and obstacle layout scaling based on difficulty."""

    @staticmethod
    def create_obstacle_pattern(
        canvas, start_x, floor_y, difficulty="MEDIUM", spacing_factor=1.0
    ):
        obstacles = []
        base_layout = [
            ("spike", 0),
            ("pad", 500),
            ("spike", 1100),
            ("double_spike", 1750),
            ("pad", 2350),
            ("triple_spike", 2950),
        ]

        for obj_type, offset in base_layout:
            if difficulty == "EASY":
                if obj_type in ["double_spike", "triple_spike"]:
                    obj_type = "spike"
            elif difficulty == "MEDIUM":
                if obj_type == "triple_spike":
                    obj_type = "double_spike"

            x = start_x + int(offset * spacing_factor)

            if obj_type == "spike":
                obstacles.append(Spike(canvas, x, floor_y - 35, 35, 35))
            elif obj_type == "double_spike":
                obstacles.append(Spike(canvas, x, floor_y - 35, 35, 35))
                obstacles.append(Spike(canvas, x + 35, floor_y - 35, 35, 35))
            elif obj_type == "triple_spike":
                obstacles.append(Spike(canvas, x, floor_y - 35, 35, 35))
                obstacles.append(Spike(canvas, x + 35, floor_y - 35, 35, 35))
                obstacles.append(Spike(canvas, x + 70, floor_y - 35, 35, 35))
            elif obj_type == "pad":
                obstacles.append(JumpPad(canvas, x, floor_y - 12))

        return obstacles


# -------------------------------------------------------------------
# Main Game Controller / Engine
# -------------------------------------------------------------------
class GeometryDashGame:
    """Central Controller managing canvas state, menus, and frame ticks."""

    DIFFICULTIES = {
        "EASY": {"speed": 6, "spacing": 1.2},
        "MEDIUM": {"speed": 8, "spacing": 1.0},
        "HARD": {"speed": 11, "spacing": 0.85},
    }

    def __init__(self, root):
        self.root = root
        self.root.title("OOP Geometry Dash")

        # Initial Dimensions
        self.width = 1200
        self.height = 600
        self.floor_y = self.height - 100
        self.target_score = 250  # Score target updated to 250
        self.is_fullscreen = False

        self.canvas = tk.Canvas(root, bg="#0D0D1A", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Dynamic Window Resize Listener
        self.canvas.bind("<Configure>", self.on_window_resize)

        # Keyboard Bindings
        self.root.bind("<space>", lambda e: self.handle_input_action())
        self.root.bind("<Return>", lambda e: self.handle_input_action())
        self.root.bind("<Up>", lambda e: self.handle_input_up())
        self.root.bind("<Down>", lambda e: self.handle_input_down())
        self.root.bind("<Escape>", lambda e: self.handle_input_esc())
        self.root.bind("<r>", lambda e: self.handle_input_r())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())

        self.state = STATE_MENU
        self.selected_difficulty = "MEDIUM"

        self.player = None
        self.obstacles = []
        self.particles = []
        self.popups = []

        self.scroll_speed = 8
        self.spacing_factor = 1.0
        self.score = 0
        self.high_score = 0
        self.level_offset = 600

        # Start maximized
        try:
            self.root.state("zoomed")
        except Exception:
            self.root.attributes("-fullscreen", True)

    def on_window_resize(self, event):
        if event.width > 100 and event.height > 100:
            self.width = event.width
            self.height = event.height
            self.floor_y = self.height - 100

            if self.player:
                self.player.ground_y = self.floor_y - 36
                if self.player.is_grounded:
                    self.player.y = self.player.ground_y

            if self.state == STATE_MENU:
                self.draw_menu()
            elif self.state in [STATE_PLAYING, STATE_PAUSED]:
                self.setup_game_ui()
            elif self.state == STATE_WIN:
                self.trigger_win()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def quit_game(self):
        self.root.destroy()

    # --- MENU & UI RENDERING ---
    def draw_menu(self):
        self.canvas.delete("all")
        self.state = STATE_MENU

        # Background Decor
        self.canvas.create_rectangle(
            0, 0, self.width, self.height, fill="#0D0D1A", outline=""
        )
        self.canvas.create_line(
            0, self.floor_y, self.width, self.floor_y, fill="#00FFCC", width=3
        )

        # Title Text
        self.canvas.create_text(
            self.width / 2,
            self.height * 0.18,
            text="GEOMETRY DASH",
            fill="#00FFCC",
            font=("Impact", max(24, int(self.height * 0.08))),
        )
        self.canvas.create_text(
            self.width / 2,
            self.height * 0.28,
            text="Reach 250 Points to Win!",
            fill="#8888AA",
            font=("Consolas", max(12, int(self.height * 0.025))),
        )

        # Difficulty Menu Selection
        self.canvas.create_text(
            self.width / 2,
            self.height * 0.38,
            text="Use UP/DOWN Arrows to Select:",
            fill="#FFFFFF",
            font=("Consolas", max(12, int(self.height * 0.025)), "bold"),
        )

        diff_y = self.height * 0.46
        for diff_name in ["EASY", "MEDIUM", "HARD"]:
            is_selected = self.selected_difficulty == diff_name
            color = "#00FF88" if is_selected else "#222233"
            text_color = "#000000" if is_selected else "#8888AA"

            btn = self.canvas.create_rectangle(
                self.width / 2 - 120,
                diff_y - 18,
                self.width / 2 + 120,
                diff_y + 18,
                fill=color,
                outline="#FFFFFF" if is_selected else "",
                width=2 if is_selected else 1,
            )
            txt = self.canvas.create_text(
                self.width / 2,
                diff_y,
                text=f"> {diff_name} <" if is_selected else diff_name,
                fill=text_color,
                font=("Impact", 18),
            )

            self.canvas.tag_bind(
                btn, "<Button-1>", lambda e, d=diff_name: self.set_difficulty(d)
            )
            self.canvas.tag_bind(
                txt, "<Button-1>", lambda e, d=diff_name: self.set_difficulty(d)
            )
            diff_y += 45

        # EXIT BUTTON
        exit_y = diff_y + 10
        exit_btn = self.canvas.create_rectangle(
            self.width / 2 - 120,
            exit_y - 18,
            self.width / 2 + 120,
            exit_y + 18,
            fill="#FF3366",
            outline="#FFFFFF",
            width=2,
        )
        exit_txt = self.canvas.create_text(
            self.width / 2,
            exit_y,
            text="EXIT GAME",
            fill="#FFFFFF",
            font=("Impact", 18),
        )
        self.canvas.tag_bind(exit_btn, "<Button-1>", lambda e: self.quit_game())
        self.canvas.tag_bind(exit_txt, "<Button-1>", lambda e: self.quit_game())

        # Prompt
        self.canvas.create_text(
            self.width / 2,
            self.height * 0.90,
            text="Press SPACE to Start | Press F11 for Fullscreen",
            fill="#FFFF00",
            font=("Consolas", max(12, int(self.height * 0.025)), "bold"),
        )

    def set_difficulty(self, diff_name):
        self.selected_difficulty = diff_name
        self.draw_menu()

    def cycle_difficulty(self, delta):
        options = ["EASY", "MEDIUM", "HARD"]
        curr_idx = options.index(self.selected_difficulty)
        new_idx = (curr_idx + delta) % len(options)
        self.set_difficulty(options[new_idx])

    def setup_game_ui(self):
        self.canvas.delete("all")

        self.canvas.create_line(
            0, self.floor_y, self.width, self.floor_y, fill="#00FFCC", width=3
        )
        self.canvas.create_rectangle(
            0,
            self.floor_y + 3,
            self.width,
            self.height,
            fill="#05050D",
            outline="",
        )

        self.score_text = self.canvas.create_text(
            30,
            30,
            text=f"SCORE: {self.score} / {self.target_score}",
            fill="#FFFFFF",
            font=("Consolas", 16, "bold"),
            anchor="w",
        )
        self.diff_display = self.canvas.create_text(
            self.width / 2,
            30,
            text=f"[{self.selected_difficulty}]",
            fill="#00FFCC",
            font=("Consolas", 14, "bold"),
        )
        self.high_score_text = self.canvas.create_text(
            self.width - 30,
            30,
            text=f"BEST: {self.high_score}",
            fill="#8888AA",
            font=("Consolas", 16, "bold"),
            anchor="e",
        )

    # --- INPUT HANDLERS ---
    def handle_input_up(self):
        if self.state == STATE_MENU:
            self.cycle_difficulty(-1)
        elif self.state == STATE_PLAYING:
            self.player.jump()

    def handle_input_down(self):
        if self.state == STATE_MENU:
            self.cycle_difficulty(1)

    def handle_input_action(self):
        if self.state == STATE_MENU:
            self.start_game()
        elif self.state == STATE_PLAYING:
            self.player.jump()
        elif self.state == STATE_PAUSED:
            self.resume_game()

    def handle_input_esc(self):
        if self.state == STATE_PLAYING:
            self.pause_game()
        elif self.state in [STATE_PAUSED, STATE_WIN]:
            self.clear_game_objects()
            self.draw_menu()

    def handle_input_r(self):
        if self.state in [STATE_GAMEOVER, STATE_WIN]:
            self.start_game()

    # --- GAME FLOW & PAUSE ---
    def start_game(self):
        self.clear_game_objects()

        cfg = self.DIFFICULTIES[self.selected_difficulty]
        self.scroll_speed = cfg["speed"]
        self.spacing_factor = cfg["spacing"]

        self.setup_game_ui()

        self.player = Player(
            self.canvas, x=120, y=self.floor_y - 36, size=36
        )
        self.score = 0
        self.state = STATE_PLAYING
        self.level_offset = 0

        self.obstacles = LevelFactory.create_obstacle_pattern(
            self.canvas,
            self.width + 100,
            self.floor_y,
            self.selected_difficulty,
            self.spacing_factor,
        )
        self.game_loop()

    def pause_game(self):
        self.state = STATE_PAUSED
        self.canvas.create_rectangle(
            self.width / 2 - 200,
            self.height / 2 - 80,
            self.width / 2 + 200,
            self.height / 2 + 80,
            fill="#000000",
            outline="#00FFCC",
            width=2,
            tags="pause_ui",
        )
        self.canvas.create_text(
            self.width / 2,
            self.height / 2 - 45,
            text="PAUSED",
            fill="#FFFF00",
            font=("Impact", 32),
            tags="pause_ui",
        )
        self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            text="Press SPACE to Resume",
            fill="#FFFFFF",
            font=("Consolas", 14),
            tags="pause_ui",
        )
        self.canvas.create_text(
            self.width / 2,
            self.height / 2 + 35,
            text="Press ESC again to Menu",
            fill="#FF8888",
            font=("Consolas", 14),
            tags="pause_ui",
        )

    def resume_game(self):
        self.canvas.delete("pause_ui")
        self.state = STATE_PLAYING
        self.game_loop()

    def spawn_particles(self, x, y, color, count=12):
        for _ in range(count):
            vx = random.uniform(-6, 6)
            vy = random.uniform(-6, 2)
            self.particles.append(Particle(self.canvas, x, y, vx, vy, color))

    # --- MAIN LOOP ---
    def game_loop(self):
        if self.state != STATE_PLAYING:
            return

        landed = self.player.update_physics()
        if landed:
            self.spawn_particles(
                self.player.x + 18, self.floor_y, "#888888", count=6
            )

        for p in self.particles[:]:
            if p.update():
                p.destroy()
                self.particles.remove(p)

        for popup in self.popups[:]:
            if popup.update():
                popup.destroy()
                self.popups.remove(popup)

        for obs in self.obstacles[:]:
            obs.update(self.scroll_speed)

            if not obs.passed and (obs.x + obs.width) < self.player.x:
                obs.passed = True
                self.score += 10
                self.canvas.itemconfig(
                    self.score_text,
                    text=f"SCORE: {self.score} / {self.target_score}",
                )

                self.popups.append(
                    ScorePopup(
                        self.canvas,
                        self.player.x + 18,
                        self.player.y - 15,
                        text="+10",
                    )
                )

                if self.score >= self.target_score:
                    self.trigger_win()
                    return

            if isinstance(obs, JumpPad):
                if obs.check_trigger(self.player):
                    self.spawn_particles(obs.x + 15, obs.y, "#FFFF00", count=10)

            elif isinstance(obs, Spike) and obs.is_colliding(self.player):
                self.trigger_game_over()
                return

            if obs.x + obs.width < -50:
                obs.destroy()
                self.obstacles.remove(obs)

        self.level_offset -= self.scroll_speed
        if self.level_offset < 400:
            new_batch = LevelFactory.create_obstacle_pattern(
                self.canvas,
                self.width + 100,
                self.floor_y,
                self.selected_difficulty,
                self.spacing_factor,
            )
            self.obstacles.extend(new_batch)
            self.level_offset = int(3600 * self.spacing_factor)

        self.root.after(16, self.game_loop)

    def trigger_game_over(self):
        self.state = STATE_GAMEOVER
        self.spawn_particles(
            self.player.x + 18,
            self.player.y + 18,
            self.player.color,
            count=30,
        )

        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.itemconfig(
                self.high_score_text, text=f"BEST: {self.high_score}"
            )

        self.canvas.create_text(
            self.width / 2,
            self.height / 2 - 10,
            text="CRASHED!",
            fill="#FF3366",
            font=("Impact", 40),
            tags="gameover_ui",
        )
        self.canvas.create_text(
            self.width / 2,
            self.height / 2 + 40,
            text="Press 'R' to Retry | Press 'ESC' for Menu",
            fill="#FFFFFF",
            font=("Consolas", 16),
            tags="gameover_ui",
        )

    def trigger_win(self):
        self.state = STATE_WIN
        self.canvas.delete("win_ui")

        if self.score > self.high_score:
            self.high_score = self.score

        # Window Box
        box_w, box_h = 440, 260
        cx, cy = self.width / 2, self.height / 2

        self.canvas.create_rectangle(
            cx - box_w / 2,
            cy - box_h / 2,
            cx + box_w / 2,
            cy + box_h / 2,
            fill="#0D0D1A",
            outline="#00FF88",
            width=3,
            tags="win_ui",
        )

        self.canvas.create_text(
            cx,
            cy - 80,
            text="LEVEL COMPLETE!",
            fill="#00FF88",
            font=("Impact", 36),
            tags="win_ui",
        )

        self.canvas.create_text(
            cx,
            cy - 30,
            text=f"Target Goal Reached: {self.score} Points",
            fill="#FFFFFF",
            font=("Consolas", 14),
            tags="win_ui",
        )

        # Interactive Button Options on Win Pop-Up
        # 1. Replay Button
        btn_replay = self.canvas.create_rectangle(
            cx - 160,
            cy + 25,
            cx - 20,
            cy + 75,
            fill="#00FF88",
            outline="#FFFFFF",
            width=2,
            tags="win_ui",
        )
        txt_replay = self.canvas.create_text(
            cx - 90,
            cy + 50,
            text="REPLAY",
            fill="#000000",
            font=("Impact", 18),
            tags="win_ui",
        )

        # 2. Main Menu Button
        btn_menu = self.canvas.create_rectangle(
            cx + 20,
            cy + 25,
            cx + 160,
            cy + 75,
            fill="#333355",
            outline="#FFFFFF",
            width=2,
            tags="win_ui",
        )
        txt_menu = self.canvas.create_text(
            cx + 90,
            cy + 50,
            text="MAIN MENU",
            fill="#FFFFFF",
            font=("Impact", 18),
            tags="win_ui",
        )

        # Event listeners for Win Window choices
        self.canvas.tag_bind(btn_replay, "<Button-1>", lambda e: self.start_game())
        self.canvas.tag_bind(txt_replay, "<Button-1>", lambda e: self.start_game())

        self.canvas.tag_bind(
            btn_menu,
            "<Button-1>",
            lambda e: [self.clear_game_objects(), self.draw_menu()],
        )
        self.canvas.tag_bind(
            txt_menu,
            "<Button-1>",
            lambda e: [self.clear_game_objects(), self.draw_menu()],
        )

    def clear_game_objects(self):
        if self.player:
            self.player.destroy()
        for obs in self.obstacles:
            obs.destroy()
        for p in self.particles:
            p.destroy()
        for pop in self.popups:
            pop.destroy()

        self.obstacles.clear()
        self.particles.clear()
        self.popups.clear()


# -------------------------------------------------------------------
# Main Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryDashGame(root)
    root.mainloop()