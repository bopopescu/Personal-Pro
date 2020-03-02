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

        #Price input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button Add Product
        ttk.Button(frame, text = 'Save Product').grid(row = 3, columnspan = 2, sticky = W+E)


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()