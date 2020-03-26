# Font directory: C:\Users\drarn\Documents\Code\Study\Kivy\kivy_venv\Lib\site-packages\kivy\data\fonts
from personalUtilities.utilities import Costants, Process
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from os import listdir
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class MyProgram(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.windows_list = Costants.windows
        self.windows_class = []
        for wl in self.windows_list:
            self.windows_class.append(type(wl, (Screen,), {}))
        self.screens = []
        [Builder.load_file(f"windows/{f}") for f in listdir("windows")]

    def build(self):
        self.icon = r'C:\Users\drarn\Documents\Code\Study\Kivy\Something\personalUtilities\Skull.ico'
        self.title = "Wanna Play"
        Window.size = 360, 640
        Window.clearcolor = [6 / 255, 0, 27 / 255, 1]
        screen_manager = ScreenManager()

        for idx, i in enumerate(self.windows_list):
            screen = self.windows_class[idx](name=i)
            self.screens.append(screen)
            screen_manager.add_widget(screen)
            Process.create_kv()
        screen_manager.current = self.windows_list[0]
        print(screen_manager.current)

        return screen_manager


class Skull(Button):
    def run_pupup(self):
        Emergent().open()


class Emergent(Popup):
    pass

if __name__ == "__main__":
    window = MyProgram()
    window.run()
