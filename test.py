from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Manager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

        for i in range(4):
            txt = 'Screen {}'.format(i)
            lbl = Label(text=txt)
            screen = Screen(name=txt)
            screen.add_widget(lbl)
            self.add_widget(screen)


class Nav(GridLayout):

    def __init__(self, sm=None, *args, **kwargs):
        super(Nav, self).__init__(*args, **kwargs)
        self.sm = sm
        self.rows = 4
        self.size_hint = (.2, 1)
        for i in range(4):
            self.add_widget(Button(text="Screen {}".format(i), on_release=self.change))

    def change(self, btn):
        self.sm.current = btn.text


class Root(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        self.orientation = "horizontal"
        sm = Manager()

        self.add_widget(Nav(sm=sm))
        self.add_widget(sm)


class TestApp(App):

    def build(App):
        return Root()


if __name__ == '__main__':
    TestApp().run()