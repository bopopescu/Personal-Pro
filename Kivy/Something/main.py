# Font directory: C:\Users\drarn\Documents\Code\Study\Kivy\kivy_venv\Lib\site-packages\kivy\data\fonts
from personalUtilities.utilities import Costants, Process, Conection
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from os import listdir
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock


class MyProgram(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count_time = 0
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
        Clock.schedule_interval(self.Callback_Clock, 2)
        return screen_manager

    def Callback_Clock(self, dt):
        self.count_time += 1
        self.screens[0].ids.time_pass.text = str(self.count_time)


class Skull(Button):
    def run_pupup(self):
        Emergent().open()


class Emergent(Popup):
    pass


class LoginButton(Button):
    def check_everything(self, username, password):
        if Process.check_nickname(username):
            print('Correct username\n')
            if Conection.check_internet():
                print('You have internet connection\n')
                cnx = Conection.abrir()
                cursor = cnx.cursor()
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result is None:
                    print("This user doesn't exist\n")
                    return False
                if result[0] == password:
                    print('You are right\n')
                    return True
                else:
                    print('Wrong password\n')
                    return False
            else:
                print('There is not internet connection. It will be used the local database\n')
                conn, c = Conection.abrir_sqlite()
                c.execute("SELECT password FROM users WHERE username = :username",
                          {'username': username})
                result = c.fetchone()

                if result is None:
                    print("This user doesn't exist\n")
                    return False
                if result[0] == password:
                    print('You are right\n')
                    return True
                else:
                    print('Wrong password\n')
                    return False
        else:
            print('invalid username')
            return False


if __name__ == "__main__":
    window = MyProgram()
    window.run()
