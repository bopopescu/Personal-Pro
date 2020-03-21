# coding: utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class FirstWindow(FloatLayout):

    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)

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
        bt.on_press = self.on_press_bt

        formato = {'text': "Hello World With Label, Text Input and Button", 'italic': True, 'font_size': 30}
        lb = Label(**formato)
        lb.size_hint = None, None
        lb.width = 400
        lb.height = 50
        lb.y = 50
        lb.x = 100

        self.add_widget(ed)
        self.add_widget(bt)
        self.add_widget(lb)

    def on_press_bt(self):
        window.root_window.remove_widget(window.root)
        window.root_window.add_widget(SecondWindow())


class SecondWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        self.orientation = "vertical"
        lb = Label(text= "Hello World Label")
        bt = Button(text="Click Here")
        bt.on_press = self.on_press_bt
        self.add_widget(lb)
        self.add_widget(bt)

    def on_press_bt(self):
        print("Hello")


class MyProgram(App):
    def build(self):
        return FirstWindow()


window = MyProgram()
window.title = "Hello"
Window.size = 600, 600
window.run()
