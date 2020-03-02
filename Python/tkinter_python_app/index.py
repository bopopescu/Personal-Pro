from tkinter import ttk
from tkinter import *

import mysql.connector

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
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button Add Product
        ttk.Button(frame, text = 'Save Product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W+E)

        #Output messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)

        self.get_products()

    #Método que establece la conexión a la base de datos
    def abrir(self):
        cnx = mysql.connector.connect(user='ucv6dyydm7ziyttq', 
                                password='VDnUMuRPNYN1GqzQYxPT',
                                host='be6v5hba1kumyfvusyeb-mysql.services.clever-cloud.com',
                                database='be6v5hba1kumyfvusyeb',
                                port=3306)
        return cnx
    
    #Método que inicializa la conexión y corre los querys
    def run_query_get(self, query):
        conex=self.abrir()
        cursor=conex.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
         
    
    def get_products(self):
        #Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #Quering data    
        query = 'SELECT * FROM inventario ORDER BY item DESC'
        db_rows = self.run_query_get(query)

        #Filling table
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):

        if self.validation():

            conex=self.abrir()
            cursor=conex.cursor()
            cursor.execute("""
                        INSERT INTO inventario(`item`, `precio`)
                            VALUES(%s,%s)
                        """,(self.name.get(),self.price.get()))
            conex.commit()
            self.get_products()
            self.message['text'] = f'El elemento {self.name.get()} fue agregado'
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
           self.message['text'] = 'El nombre y precio son requeridos'
  


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()