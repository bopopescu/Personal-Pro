# coding: utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label


class MyProgram(App):

    @staticmethod
    def click():
        print('Hi')

    def build(self):
        layout = FloatLayout()

        ed = TextInput(text="Hello World")
        ed.size_hint = None, None
        ed.height = 300
        ed.width = 400
        ed.x = 100
        ed.y = 250

        bt = Button(text="Click")
        bt.size_hint = None, None
        bt.width = 200
        bt.height = 50
        bt.y = 150
        bt.x = 200
        bt.on_press = MyProgram.click

        formato = {'text': "Hello World With Label, Text Input and Button", 'italic': True, 'font_size': 30}
        lb = Label(**formato)
        lb.size_hint = None, None
        lb.width = 400
        lb.height = 50
        lb.y = 50
        lb.x = 100

        layout.add_widget(ed)
        layout.add_widget(bt)
        layout.add_widget(lb)
        return layout


window = MyProgram()
window.title = "Hello"
Window.size = 600, 600
window.run()
