# coding: utf-8

from kivy.app import App
from kivy.uix.label import Label


def build():
    # Form One
    # lb = Label(text = "Curso de Python e Kivy", italic = True, font_size = 50)

    # Form Two
    # lb = Label()
    # lb.text = "Curso de Python e Kivy"
    # lb.italic = True
    # lb.font_size = 50

    # Form Three
    formato = {'text': "Curso de Python e Kivy", 'italic': True, 'font_size': 50}
    lb = Label(**formato)
    return lb


hello_world = App()
hello_world.build = build
hello_world.run()
