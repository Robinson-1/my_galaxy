from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)
    
    def open_popup(self):
        pops = OptionsPopup()
        pops.open()

class OptionsPopup(Popup):
    pass

class PopUpWindow(App):
    def build(self):

        return MenuWidget()