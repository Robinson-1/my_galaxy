from kivy.config import Config
from kivy.lang import Builder

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.properties import  StringProperty

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from game import GameWidget

Builder.load_file("game.kv")

class StartWindow(Screen):
    menu_title = StringProperty("G   A   L   A   X   Y")
    play_button_title = StringProperty("PLAY")

class GameWindow(Screen):
    pass

kv = Builder.load_file("main.kv")

class GalaxyApp(App):
    def build(self):
        return kv

GalaxyApp().run()
