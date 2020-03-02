from tkinter import ttk
from tkinter import *

class Product:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        #Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Register a new product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 1)


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()