from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from collections import OrderedDict
from pymongo import MongoClient
from utils.datatable import DataTable

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        #Display Products
        product_scrn = self.ids.scrn_product_content
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)
    
    def add_user_fields(self):
        target = self.ids.ops_fields
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_des = Spinner(text='Operator',values=['Operator','Administrator'])

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)


    def get_users(self):
        client = MongoClient()
        db = client.SilverPos
        users = db.users

        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['passwords'] = {}
        _users['designations'] = {}


        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd)>10:
                pwd = pwd[:10]+'...'
            passwords.append(pwd)
            designations.append(user['designation'])
        

        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users['first_names'][idx]=first_names[idx]
            _users['last_names'][idx]=last_names[idx]  
            _users['user_names'][idx]=user_names[idx]  
            _users['passwords'][idx]=passwords[idx]  
            _users['designations'][idx]=designations[idx]      
            idx +=1
        return _users
    
    def get_products(self):
        client = MongoClient()
        db = client.SilverPos
        products = db.stocks

        _stocks = OrderedDict()

        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['order'] = {}
        _stocks['last_purchase'] = {}

        product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []

        for product in products.find():
            product_code.append(product['product_code'])
            name = product['product_name']
            if len(name) > 10:
                name = name[:10]+'...'
            product_name.append(name)
            product_weight.append(product['product_weight'])
            in_stock.append(product['in_stock'])
            sold.append(product['sold'])
            order.append(product['order'])
            last_purchase.append(product['last_purchase'])
        

        products_length = len(product_code)
        idx = 0
        while idx < products_length:
            _stocks['product_code'][idx]=product_code[idx]
            _stocks['product_name'][idx]=product_name[idx]  
            _stocks['product_weight'][idx]=product_weight[idx]  
            _stocks['in_stock'][idx]=in_stock[idx]  
            _stocks['sold'][idx]=sold[idx]
            _stocks['order'][idx]=order[idx]  
            _stocks['last_purchase'][idx]=last_purchase[idx]          
            idx +=1
        return _stocks

    def change_screen(self, instance):
        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'
    
        
        

        

class AdminApp(App):
    def build(self):
        return AdminWindow()

if __name__ == '__main__':
    AdminApp().run()