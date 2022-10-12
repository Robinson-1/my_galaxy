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

    def open_popup(self):
        pops = ScorePopup()
        pops.open()

class GameWindow(Screen):
    pass

class ScorePopup(Popup):

    SCORE_FILENAME = r'./highscores.csv'
    header_txt = ["Name", "Date", "Score"]
    score_header = StringProperty(f"{header_txt[0]:<5}{header_txt[1]:^127}{header_txt[2]}")

    def read_scores(self):
        with open(self.SCORE_FILENAME, "r") as file:
            lines = file.readlines()
            output = ""
            for line in lines:
                temp = line.split(",")
                output += f"{temp[0]:<15}{temp[1]:^125}{temp[2]:>10}"
    
        return output

kv = Builder.load_file("main.kv")

class GalaxyApp(App):
    def build(self):
        return kv

GalaxyApp().run()
