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
                

def view_inventory():
    print('\n')
    
    while True:

        print('*' * 25, '(INVENTORY MENU)', '*' * 25) 
        print('''
            Enter "A" to view all current inventory products
            Enter "S" to view all current stock available
            Enter "P"  to view all current inventory prices
            Enter "0" to exit inventory menu:
            ''')
        inventory_commands = input('Enter command: ')
        if inventory_commands.lower() == 'a':
            for item in Product.select():
                print('Date added:', '\t', 'Product name:')
                print(item.product_dates, '\t', item.product_names)
                
        elif inventory_commands.lower() == 's':
            for item in Product.select():
                print('Available Stock:', '\t\t', 'Product names:')
                print(item.product_quantity, '\t\t\t\t', item.product_names)
                
        elif inventory_commands.lower() == 'p':
            for item in Product.select():
                print('Current price:', '\t\t', 'Product names:')
                print(item.product_prices, '\t\t\t', item.product_names)
                
        elif inventory_commands.lower() == '0':
            print('\nLeaving inventory menu...\n')
            break
        else:
            print('Please enter a valid command')
            
            
            
def search_inventory(search_query = None):
    print('\n')
    while True:
        print('*' * 25, '(SEARCH MENU)', '*' * 25)
        print('''
            Search anything within the store.
            
                          OR
                        
            Press "0" to exit search menu.
        ''')
        #items = Product.select().order_by(Product.timestamp.decs())
        #if search_query:
            #items = items.where(Product.content.contains(search_query
        item_search = input('Search item(s): ')
        
        if item_search == '0':
            print('\nLeaving search menu...\n\n')
            break
    

def edit_inventory():
    print('\n')
    while True:
        print('*' * 25, '(EDIT MENU)', '*' * 25)
        print('''
            Press "A" to add a product.
            Press "E" to edit a product.
            Press "D" to delete a product.
            
                        OR
            Press "0" to exit edit menu
        ''')
        
        edit_controls = input('Enter command: ')
        
        if edit_controls.lower() == 'a':
            #print('enter your entry. press CTRL+D when finished')
            #data = sys.stdin.read().strip()
            #if data:
                #if input('\nSave entry? [Yn] ').lower() != 'n':
                #Entry.create(content = data)
                #print('Saved successfully')
                pass
        elif edit_controls.lower() == 'e':
            pass
        elif edit_controls.lower() == 'd':
            pass
        elif edit_controls == '0':
            print('\nLeaving control menu...\n\n')
            break
        else:
            print('\nPlease enter a valid command\n')
        
            


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
            view_inventory()
        elif user_input.lower() == 's':
            search_inventory()
        elif user_input.lower() == 'e':
            edit_inventory()
        elif user_input.lower() == 'q':
            sys.exit('\nExiting application...\n')
        else:
            print('\nPlease enter a valid command!\n')

        
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    menu_interface()
