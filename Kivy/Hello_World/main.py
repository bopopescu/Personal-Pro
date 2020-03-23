# coding: utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from os import listdir


class FirstWindow(FloatLayout):

    def on_press_bt(self):
        window.root_window.remove_widget(window.root)
        window.root_window.add_widget(SecondWindow())


class SecondWindow(BoxLayout):

    def on_press_bt(self):
        print("Hello")


class MyProgram(App):
    def build(self):
        return FirstWindow()


[Builder.load_file(f"windows/{f}") for f in listdir("windows")]
window = MyProgram()
window.title = "Hello"
Window.size = 600, 600
Window.clearcolor = [1, 1, 1, 1]
window.run()
