from peewee import *
import datetime
import csv
import sys
import re

db = SqliteDatabase('inventory.db')
class Product(Model):
    product_names = CharField(unique = True)
    product_quantity = IntegerField(unique = True)
    product_prices = IntegerField(unique = True)
    product_dates = DateField(unique = True)
    class Meta():
        database = db
        

def all_inventory():
    with open('inventory.csv', 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        next(file_reader)
        for item in file_reader:
            foods = item[0]
            food_cost = int(re.sub('[^0-9]','',item[1]))
            item_stock = int(item[2])
            added_dates = item[3]
            try:
                inventory = Product.create(product_names = foods, product_quantity = item_stock, product_prices = food_cost, product_dates = added_dates)
            # try to create the Product
            except IntegrityError: # if it fails do nothing
                pass
            else: #if it doesn't fail, save it
                inventory.save()
                

def view_all():
    print('\n')
    
    while True:

        print('*' * 25, '(INVENTORY MENU)', '*' * 25) 
        user_input = input('''
            Enter "A" to view all current inventory products
            Enter "S" to view all current stock available
            Enter "P"  to view all current inventory prices
            Enter "Q" to exit Inventory sub-menu:
            ''')

        if user_input.lower() == 'a':
            for item in Product.select():
                print('Date added:', '\t', 'Product name:')
                print(item.product_dates, '\t', item.product_names)
                
        elif user_input.lower() == 's':
            for item in Product.select():
                print('Available Stock:', '\t\t', 'Product names:')
                print(item.product_quantity, '\t\t\t\t', item.product_names)
                
        elif user_input.lower() == 'p':
            for item in Product.select():
                print('Current price:', '\t\t', 'Product names:')
                print(item.product_prices, '\t\t\t', item.product_names)
                
        elif user_input.lower() == 'q':
            print('\n')
            break
        else:
            print('Please enter a valid option')
            
            
            
def search_inventory():
    print('\n')
    while True:
        print('*' * 25, '(SEARCH MENU)', '*' * 25)
        print('''
            Search anything within the store.
            
                          OR
                        
            Press "E" to exit search menu.
        ''')
        item_search = input('Search item(s): ')
        if item_search.lower() == 'e':
            print('\nLeaving search menu...\n\n')
            break
    

def edit_inventory():
    pass
def menu_interface():
    while True:
        print('*' * 25, '(STORE MENU)', '*' * 25)
        print('Please select an option below:')
        print('''
              Press "V" to view all store inventory.
              Press "S" to search for products.
              Press "E" to edit store inventory.
              Press "Q" to exit application.
              ''')
        user_input = input('Menu Select: ')
        
        if user_input.lower() == 'v':
            view_all()
        elif user_input.lower() == 's':
            search_inventory()
        elif user_input.lower() == 'e':
            pass
        elif user_input.lower() == 'q':
            sys.exit('\nExiting application...\n')

        
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    menu_interface()
