import random

from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.widget import Widget

Builder.load_file("menu.kv")

class GameWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up, keyboard_closed
    from highscores import check_highscore, update_highscores

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    score_popup = ObjectProperty()
    score_button_title = StringProperty("Highscores")
    score_title = StringProperty("OPTIONS")

    V_NB_LINES = 12 # even only
    V_LINES_SPACING = .25  # % of screen
    vertical_lines = []

    H_NB_LINES = 10
    H_LINES_SPACING = .2  # % of screen
    horizontal_lines = []

    current_offset_y = 0
    current_y_loop = 0

    START_SPEED = 3

    speed = START_SPEED

    current_offset_x = 0
    current_speed_x = 0
    SPEED_X = 10

    NB_TILES = 15
    tiles = []
    tiles_coordinates = []

    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04

    ship = None
    ship_coordinaates = [(0,0) , (0,0), (0,0)]

    state_game_over = False
    state_game_started = False

    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")
    score_txt = StringProperty()
    highscore_txt = StringProperty()

    sounds_begin = None
    sounds_galaxy = None
    sounds_gameover_impact = None
    sounds_gameover_voice = None
    sounds_music1 = None
    sounds_restart = None

    SCORE_FILENAME = r'./highscores.csv'
    player_name = 'default'

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.highscore_txt = "Highscore: " + str(self.check_highscore())

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.sounds_galaxy.play()
    
    def init_audio(self):
        self.sounds_begin = SoundLoader.load("audio/begin.wav")
        self.sounds_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.sounds_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sounds_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
        self.sounds_music1 = SoundLoader.load("audio/music1.wav")
        self.sounds_restart = SoundLoader.load("audio/restart.wav")

        self.sounds_begin.volume = 0.8
        self.sounds_galaxy.volume = .25
        self.sounds_gameover_impact.volume = .8
        self.sounds_gameover_voice.volume = .8 
        self.sounds_music1.volume = .25
        self.sounds_restart.volume = .25

    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0

        self.current_offset_x = 0
        self.current_speed_x = 0

        self.speed = self.START_SPEED
        
        self.tiles_coordinates = []

        self.score_txt = "SCORE: " + str(self.current_y_loop )

        
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        x0 = self.perspective_point_x

        self.ship_coordinaates[0] = (x0 - self.SHIP_WIDTH*self.width/2, self.SHIP_BASE_Y*self.height)
        self.ship_coordinaates[1] = (x0, (self.SHIP_BASE_Y + self.SHIP_HEIGHT)*self.height)
        self.ship_coordinaates[2] = (x0 + self.SHIP_WIDTH*self.width/2, self.SHIP_BASE_Y*self.height)

        x1, y1 = self.transform(*self.ship_coordinaates[0])
        x2, y2 = self.transform(*self.ship_coordinaates[1])
        x3, y3 = self.transform(*self.ship_coordinaates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self,):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        for i in range(0, 3):
            px, py = self.ship_coordinaates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())
    
    def pre_fill_tiles_coordinates(self):
        for i in range(0,10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):

        last_y = 0
        last_x = 0
        start_index = -int(self.V_NB_LINES/2) + 1
        end_index = start_index + self.V_NB_LINES - 2

        for i in range(len(self.tiles_coordinates) -1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
        
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(-1, 1) if last_x not in [start_index, end_index] else -last_x/abs(last_x)
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y)) 
            if r == -1:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y)) 
            last_y += 1

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())
    
    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING*self.width
        offset = index - 0.5
        line_x = central_line_x + offset*spacing + self.current_offset_x
        return line_x
    
    def get_line_y_from_index(self, index):

        line_y = self.H_LINES_SPACING * index * self.height - self.current_offset_y
        return line_y
    
    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop 
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y
    
    def update_tiles(self):
        for i in range(0, self.NB_TILES):

            tile = self.tiles[i]
            tiles_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tiles_coordinates[0], tiles_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tiles_coordinates[0] + 1, tiles_coordinates[1] + 1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        start_index = -int(self.V_NB_LINES/2) + 1
        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]
    
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())
    
    def update_horizontal_lines(self):

        start_index = -int(self.V_NB_LINES/2) + 1
        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(start_index + self.V_NB_LINES -1)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        self.update_horizontal_lines()
        self.update_vertical_lines()
        self.update_tiles()
        self.update_ship()
        time_factor = dt*60
        self.speed += dt/10

        if not self.state_game_over and self.state_game_started:
            self.current_offset_y += self.speed * time_factor * self.height/400
            self.current_offset_x += self.current_speed_x * time_factor * self.width/900
            
            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "SCORE: " + str(self.current_y_loop)
        
        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_widget.opacity = 1
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.menu_button_title = "RESTART"
            self.sounds_music1.stop()
            self.sounds_gameover_impact.play()
            Clock.schedule_once(self.play_gamover_voice_sound, 1)
            self.update_highscores()
            self.highscore_txt = "Highscore: " + str(self.check_highscore())
    
    def play_gamover_voice_sound(self, dt):
        if self.state_game_over:
            self.sounds_gameover_voice.play()
    
    def on_menu_button_pressed(self):
        if self.state_game_over:
            self.sounds_restart.play()
        else:
            self.sounds_begin.play()
        self.sounds_music1.play()
        self.state_game_started = True
        self.menu_widget.opacity = 0
        self.reset_game()
