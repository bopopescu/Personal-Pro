import os
from pathlib import Path
import mysql.connector
import re
import urllib.request
import sqlite3



class Costants:
    windows = ['Login', 'Panel', 'Info']


class Process:
    @staticmethod
    def create_kv():
        for v in Costants.windows:
            if not os.path.exists(f'windows/{v}.kv'):
                Path(f'windows/{v}.kv').touch()

    @staticmethod
    def check_nickname(string):
        if re.search(r'^\w+$', string) is not None:
            return True
        return False

    @staticmethod
    def check_password(string):
        if re.search(r'[^(\w,-,.)]', string) is None:
            return True
        return False


class Conection:
    @staticmethod
    def check_internet():
        try:
            if urllib.request.urlopen('http://216.58.192.142').getcode() == 200:
                return True
        except urllib.error.URLError:
            return False


    @staticmethod
    def abrir():
        cnx = mysql.connector.connect(user='ucv6dyydm7ziyttq',
                                      password='VDnUMuRPNYN1GqzQYxPT',
                                      host='be6v5hba1kumyfvusyeb-mysql.services.clever-cloud.com',
                                      database='be6v5hba1kumyfvusyeb',
                                      port=3306)
        return cnx

    @staticmethod
    def abrir_sqlite():
        conn = sqlite3.connect('personalUtilities/BaseDeDatos.db')
        c = conn.cursor()
        return conn, c

    @staticmethod
    def add_user(username, password):
        conn, c = Conection.abrir_sqlite()
        with conn:
            c.execute("INSERT INTO users VALUES (NULL, :username, :password)",
                      {'username': username, 'password': password})
