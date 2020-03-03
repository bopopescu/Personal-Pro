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

        #Buttons
        ttk.Button(text = 'DELETE', command = self.delete_product).grid(row = 5, column = 0, sticky = W+E)
        ttk.Button(text = 'EDIT', command = self.edit_product).grid(row = 5, column = 1, sticky = W+E)
       
       
       #Filling rows
        self.get_products()


    def cleaning(self):
        #Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)


    #Método que establece la conexión a la base de datos
    def abrir(self):
        cnx = mysql.connector.connect(user='ucv6dyydm7ziyttq', 
                                password='VDnUMuRPNYN1GqzQYxPT',
                                host='be6v5hba1kumyfvusyeb-mysql.services.clever-cloud.com',
                                database='be6v5hba1kumyfvusyeb',
                                port=3306)
        return cnx
    
    #Método que inicializa la conexión y corre los querys
    def run_query_get(self, query, tipo):
        conex=self.abrir()
        cursor=conex.cursor()
        cursor.execute(query)

        if tipo:
            result = cursor.fetchall()
            return result

        conex.commit()
         
    
    def get_products(self):
        self.cleaning()

        #Quering data    
        query = 'SELECT * FROM inventario ORDER BY item DESC'
        db_rows = self.run_query_get(query, True)

        #Filling table
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):

        if self.validation():

            conex=self.abrir()
            cursor=conex.cursor()
            query = f"INSERT INTO inventario(`item`, `precio`) VALUES ('{self.name.get()}','{self.price.get()}')"
            self.run_query_get(query, False)
            self.get_products()
            self.message['text'] = f'El elemento {self.name.get()} fue agregado'
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
           self.message['text'] = 'El nombre y precio son requeridos'
    
    def delete_product(self):
        self.message['text']=''
        try:
            texto = self.tree.item(self.tree.selection())['text'][0]
            texto = self.tree.item(self.tree.selection())['text']
            conex=self.abrir()
            cursor=conex.cursor()
            query = f"DELETE FROM inventario WHERE item = '{texto}'"
            self.run_query_get(query, False)
            self.get_products()
            self.message['text'] = f'El elemento {texto} fue eliminado'

        except IndexError:
            self.message['text'] = 'Select an item to delete'
            return
    
    def edit_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Select an item to edit'
            return  
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        #New window
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'

        #Creating a Frame Container
        frame_edit = LabelFrame(self.edit_wind, text = 'Edit a product', bd=4)
        frame_edit.grid(row = 0, column = 0, columnspan = 8, padx=20, pady=20)

        #Old name
        Label(frame_edit, text = 'Old Name: ').grid(row = 0, column = 1)
        Entry(frame_edit, textvariable = StringVar(frame_edit, value = name), state = 'readonly').grid(row = 0, column = 2)


        #New name
        Label(frame_edit, text = 'New Name: ').grid(row = 1, column = 1)
        new_name = Entry(frame_edit)
        new_name.focus()
        new_name.grid(row = 1, column = 2)

        #Old price
        Label(frame_edit, text = 'Old Price: ').grid(row=2, column=1)
        Entry(frame_edit, textvariable = StringVar(frame_edit, value = old_price), state = 'readonly').grid(row=2, column=2)
        #New Price
        Label(frame_edit, text = 'New Price: ').grid(row = 3, column = 1)
        new_price = Entry(frame_edit)
        new_price.grid(row = 3, column = 2)

        #Button
        Button(frame_edit, text = 'Update', command = lambda: self.edit_records(new_name.get(),name, new_price.get(), old_price)).grid(row = 4, columnspan = 3, sticky = W+E)

    def edit_records(self, new_name, name, new_price, old_price):
        query = f"UPDATE inventario SET item = '{new_name}', precio ='{new_price}' WHERE item = '{name}' AND precio = '{old_price}'"
        self.run_query_get(query,False)
        self.edit_wind.destroy()
        self.message['text'] = f'Item {new_name} ha sido actualizado'
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()  