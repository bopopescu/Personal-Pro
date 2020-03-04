import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import  Button
from kivy.uix.screenmanager import ScreenManager, Screen

import mysql.connector

class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text = "IP: "))
        self.ip = TextInput(multiline=False)
        self.add_widget(self.ip)

        self.add_widget(Label(text = "Port: "))
        self.port = TextInput(multiline=False)
        self.add_widget(self.port)

        self.add_widget(Label(text = "Username: "))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text = "Password: "))
        self.password = TextInput(multiline=False)
        self.add_widget(self.password)

        self.join = Button(text = "Join")
        self.join.bind(on_press = self.join_button)
        self.add_widget(Label())
        self.add_widget(self.join)

        self.get_one_user()



###
####
# Lógica de la base de datos
####
###


    def abrir(self):
        cnx = mysql.connector.connect(user='ucv6dyydm7ziyttq', 
                                password='VDnUMuRPNYN1GqzQYxPT',
                                host='be6v5hba1kumyfvusyeb-mysql.services.clever-cloud.com',
                                database='be6v5hba1kumyfvusyeb',
                                port=3306)
        return cnx
    
    def run_query_get(self, query, tipo):
        conex=self.abrir()
        cursor=conex.cursor()
        cursor.execute(query)

        if tipo:
            result = cursor.fetchall()
            return result

        conex.commit()
   
    def get_one_user(self):
        query = "SELECT * FROM usuarios WHERE user_id = '1'"
        db_rows = self.run_query_get(query, True)
        for row in db_rows:
            self.ip.text = row[1]
            self.port.text = row[2]
            self.username.text = row[3]
            self.password.text = row[4]

    def add_user(self):
        query = f"INSERT INTO usuarios(`ip`, `port`,`username`, `password`) VALUES ('{self.ip.text}','{self.port.text}','{self.username.text}','{self.password.text}')"
        self.run_query_get(query, False)
    




###
####
# Lógica de la base de datos
####
###
    


    def join_button(self, instance):
        #self.add_user()
        info = f"Attempting to join {self.ip.text}:{self.port.text} as {self.username.text} with password: {self.password.text}"
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = "Info"


class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center",valign="middle",font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
    
    def update_info(self, message):
        self.message.text = message
    
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)


class EpicApp(App):
    def build(self):

         self.screen_manager = ScreenManager()
         self.connect_page = ConnectPage()
         screen = Screen(name = "Connect")
         screen.add_widget(self.connect_page)
         self.screen_manager.add_widget(screen)

         self.info_page = InfoPage()
         screen = Screen(name = 'Info')
         screen.add_widget(self.info_page)
         self.screen_manager.add_widget(screen)

         return self.screen_manager

if __name__ == "__main__":
    chat_app = EpicApp()
    chat_app.run()