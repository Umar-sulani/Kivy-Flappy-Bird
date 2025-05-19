from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from random import randint


class Bird(Image):
    velocity = NumericProperty(0)
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
        with self.canvas.after:
            PopMatrix()
        self.rot.origin = self.center
        self.target_angle = 0

    def move(self):
        self.y += self.velocity
        self.velocity -= self.parent.gravity

        # Rotate bird based on velocity
        self.target_angle = max(min(self.velocity * 3, 30), -90)
        Clock.schedule_once(self.smooth_rotate, 0)
        self.rot.origin = self.center

    def smooth_rotate(self, dt):
        lerp_speed = 0.2
        self.angle += (self.target_angle - self.angle) * lerp_speed
        self.rot.angle = self.angle


class Pipe(Image):
    flip = BooleanProperty(False)


class ScoreBox(Widget):
    score_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 1)  # Black background
            self.bg = Rectangle()
        self.score_label = Label(text="0", color=(1, 1, 1, 1), font_size=30)
        self.add_widget(self.score_label)

    def update_size_pos(self, parent):
        self.size = (parent.width, 50)
        self.pos = (0, 0)
        self.bg.size = self.size
        self.bg.pos = self.pos
        self.score_label.center = (self.center_x, self.y + 25)


class GameScreen(Widget):
    bird = ObjectProperty(None)
    pipes = ListProperty([])
    score = NumericProperty(0)
    background = ObjectProperty(None)
    game_over_label = ObjectProperty(None)
    game_running = BooleanProperty(False)
    gravity = NumericProperty(0)
    base_width = 400
    base_height = 600
    scale = NumericProperty(1)
    score_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize(Window, Window.width, Window.height)

        # Add ScoreBox widget
        self.score_box = ScoreBox()
        self.add_widget(self.score_box)

    def on_window_resize(self, window, width, height):
        self.scale = min(width / self.base_width, height / self.base_height)
        self.gravity = 0.5 * self.scale

        if self.bird:
            self.bird.size = (80 * self.scale, 80 * self.scale)
            self.bird.pos = (100 * self.scale, self.height / 2)
            self.bird.rot.origin = self.bird.center

        if self.score_box:
            self.score_box.update_size_pos(self)

    def start_game(self):
        self.clear_pipes()
        self.reset_bird()
        self.score = 0
        if self.game_over_label:
            self.game_over_label.opacity = 0
        self.game_running = True

        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.create_pipe, 2)
        Clock.schedule_interval(self.update_score, 0.5)

    def on_touch_down(self, touch):
        if not self.game_running:
            self.start_game()
        self.bird.velocity = 10 * self.scale

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if not self.game_running:
            self.start_game()
        if key == 32:
            self.bird.velocity = 10 * self.scale

    def create_pipe(self, dt):
        gap_height = 250 * self.scale
        min_pipe_height = 80 * self.scale
        max_pipe_height = self.height - gap_height - min_pipe_height
        top_pipe_height = randint(int(min_pipe_height), int(max_pipe_height))
        bottom_pipe_height = self.height - top_pipe_height - gap_height

        pipe_width = 150 * self.scale

        top_pipe = Pipe(source='pipe.png')
        top_pipe.size = (pipe_width, top_pipe_height)
        top_pipe.pos = (self.width, self.height - top_pipe_height)
        top_pipe.flip = True

        bottom_pipe = Pipe(source='pipe.png')
        bottom_pipe.size = (pipe_width, bottom_pipe_height)
        bottom_pipe.pos = (self.width, 0)

        self.add_widget(top_pipe)
        self.add_widget(bottom_pipe)
        self.pipes.append((top_pipe, bottom_pipe))

    def update(self, dt):
        self.bird.move()

        move_speed = 3 * self.scale

        for pair in self.pipes:
            for pipe in pair:
                pipe.x -= move_speed
                if self.bird.collide_widget(pipe):
                    self.game_over()

        self.pipes = [pair for pair in self.pipes if pair[0].x + pair[0].width > 0]

        if self.bird.y < 0 or self.bird.top > self.height:
            self.game_over()

        self.score_box.score_label.text = str(self.score)

    def update_score(self, dt):
        self.score += 1

    def game_over(self):
        if not self.game_running:
            return

        if self.game_over_label:
            self.game_over_label.opacity = 1

        Clock.unschedule(self.update)
        Clock.unschedule(self.create_pipe)
        Clock.unschedule(self.update_score)
        self.game_running = False

    def clear_pipes(self):
        for pair in self.pipes:
            for pipe in pair:
                self.remove_widget(pipe)
        self.pipes.clear()

    def reset_bird(self):
        self.bird.size = (80 * self.scale, 80 * self.scale)
        self.bird.pos = (100 * self.scale, self.height / 2)
        self.bird.velocity = 0
        self.bird.angle = 0
        self.bird.target_angle = 0
        self.bird.rot.origin = self.bird.center
        self.bird.rot.angle = 0


class FlappyApp(App):
    def build(self):
        return GameScreen()


if __name__ == "__main__":
    FlappyApp().run()
