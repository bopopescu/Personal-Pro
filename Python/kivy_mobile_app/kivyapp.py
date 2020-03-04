import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import  Button

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
        port = self.port.text
        ip = self.ip.text
        username = self.username.text
        password = self.password.text
        print(port, ip, username,password)
        self.add_user()


class EpicApp(App):
    def build(self):
        return ConnectPage()

if __name__ == "__main__":
    EpicApp().run()