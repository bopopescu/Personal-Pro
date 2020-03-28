# Font directory: C:\Users\drarn\Documents\Code\Study\Kivy\kivy_venv\Lib\site-packages\kivy\data\fonts
# Font URL: https://github.com/google/fonts/blob/master/ofl/solway/Solway-Regular.ttf

import personalUtilities.utilities
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from os import listdir
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner


class MyProgram(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count_time = 0
        self.windows_list = personalUtilities.utilities.Costants.windows
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
        self.screen_manager = ScreenManager()

        for idx, i in enumerate(self.windows_list):
            screen = self.windows_class[idx](name=i)
            self.screens.append(screen)
            self.screen_manager.add_widget(screen)
            personalUtilities.utilities.Process.create_kv()
        self.screen_manager.current = self.windows_list[0]
        Clock.schedule_interval(self.Callback_Clock, 2)
        return self.screen_manager

    def Callback_Clock(self, dt):
        self.count_time += 1
        self.screens[0].ids.time_pass.text = str(self.count_time)

    def LoadData(self):
        conn, c = personalUtilities.utilities.Conection.abrir_sqlite()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()

        container_id = self.screens[2].ids.container_grid

        container_id.bind(minimum_height=container_id.setter('height'))
        for user_info in result:
            user_name = Button(text=user_info[1], halign="center", valign="middle", size_hint=(None, None),
                               size=(126, 20), color=(1, 1, 1, 0.85), font_size=14, font_name="Solway-Regular",
                               on_release=self.buttonEdit)
            lab = Label(text=user_info[2], halign="center", valign="middle", size_hint=(None, None),
                        size=(93.85, 14), color=(1, 1, 1, 0.85), font_size=12, font_name="Solway-Regular",
                        text_size=(93.85, 14))
            spin = Spinner(text=str(user_info[3]), values=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                           halign="center", valign="middle", size_hint=(None, None), size=(23, 20),
                           color=(1, 1, 1, 0.85), font_size=16, font_name="Solway-Regular", id=str(user_info[0]))

            container_id.add_widget(user_name)
            container_id.add_widget(lab)
            container_id.add_widget(spin)
            spin.bind(text=self.show_selected_value)

        self.screen_manager.current = 'Info'

    def buttonEdit(self, obj):
        self.obj = obj
        pup = EmergentEdit()
        pup.ids.input_username.text = obj.text
        pup.ids.input_username.on_text_validate = pup.on_text_validate
        pup.open()

    @staticmethod
    def show_selected_value(spinner, text):
        text = int(text)
        id_user = int(spinner.id)
        conn, c = personalUtilities.utilities.Conection.abrir_sqlite()
        cursor = conn.cursor()
        cursor.execute("UPDATE users set times = :text WHERE id_user = :id_user",
                       {'text': text, 'id_user': id_user})
        conn.commit()

    def chage_color(self, *colors):
        self.screens[2].ids.color_try.canvas.before.children[0].rgb = [(int(colors[0]) / 255), (int(colors[1]) / 255),
                                                                       (int(colors[2]) / 255)]

    @staticmethod
    def save_cloud():
        if personalUtilities.utilities.Conection.check_internet():
            conn, c = personalUtilities.utilities.Conection.abrir_sqlite()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            local = cursor.fetchall()

            cnx = personalUtilities.utilities.Conection.abrir()
            cursor = cnx.cursor()
            for loc in local:
                print(loc)
                cursor.execute("UPDATE users SET username = %s, times = %s WHERE id_user = %s;", (loc[1], loc[3],
                                                                                                  loc[0]))
                cnx.commit()


class EmergentEdit(Popup):
    def on_text_validate(self):
        old_username = window.obj.text
        new_username = self.ids.input_username.text
        if personalUtilities.utilities.Process.check_nickname(new_username):
            window.obj.text = new_username
            conn, c = personalUtilities.utilities.Conection.abrir_sqlite()
            cursor = conn.cursor()
            cursor.execute("UPDATE users set username = :new_username WHERE username = :old_username",
                           {'new_username': new_username, 'old_username': old_username})
            conn.commit()
        self.dismiss()


class Skull(Button):

    @staticmethod
    def run_pupup():
        Emergent().open()


class Emergent(Popup):
    pass


class LoginButton(Button):

    @staticmethod
    def check_everything(username, password):
        if personalUtilities.utilities.Process.check_nickname(username):
            print('Correct username\n')
            if personalUtilities.utilities.Conection.check_internet():
                print('You have internet connection\n')
                cnx = personalUtilities.utilities.Conection.abrir()
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
                conn, c = personalUtilities.utilities.Conection.abrir_sqlite()
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
