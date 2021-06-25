from peewee import *
import datetime
import csv
import sys
import re
import os

#to-do list

#(TOP PRIORITY)
#figure out how to save and update existing items with new data
#how to delete items within DB
#figure out product_id

#(functionality)
#show stock of items
#show dates of items
#show price of items

#(finishing touches)
#backup whole database to a csv file
#documentation of code via doctext
#find errors
#clean code


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

db = SqliteDatabase('inventory.db')
class Product(Model):
    #product_id = AutoField()
    product_quantity = IntegerField(unique = True)
    product_price = IntegerField()
    date_updated = DateField()
    product_name = CharField(unique = True)
    class Meta:
        database = db
        
def csv_extractor():
    with open('inventory.csv', 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        next(file_reader)
        for item in file_reader:
            foods = item[0]
            food_cost = int(re.sub('[^0-9]','',item[1]))
            item_stock = int(item[2])
            added_dates = item[3]
            
            #adds information from the csv into the attributes needed in the database and handles errors
            try:
                inventory = Product.create(product_name = foods, product_quantity = item_stock, product_price = food_cost, date_updated = added_dates)
            # try to create the Product
            except IntegrityError: # if it fails do nothing
                pass
            else: #if it doesn't fail, save it
                inventory.save()

def main_menu():
    while True:
        print('Welcome to the store inventory')
        program_start = input('To start the program click "S" to start: ')
        if program_start.lower() == 's':
            break
        else:
            clear()
            print('*'* 25, 'Please enter a valid option!', '*' *25, '\n')
    if program_start.lower() == 's':
        clear()
        print('*' * 25,'Store Inventory', '*' * 25)
        while True:
            print('''Main Menu:
                Press "V" to view product information.
                Press "A" to add a new product to the database.
                Press "B" to backup the database to a CSV file.
                Press "0" to quit the application.''')
                
            option_select = input('\nPlease select an option above: ')
            if option_select.lower() == 'v':
                clear()
                item_search_menu()
            elif option_select.lower() == 'a':
                clear()
                add_product_menu()
            elif option_select.lower() == 'b':
                clear()
            elif option_select.lower() == '0':
                clear()
                sys.exit('Leaving application...')
            else:
                print('Please select a valid option!')

def search(search_query = None):
    all_items = Product.select()
    print('*' * 25,'Item Searched','*' * 25)
    if search_query:
        all_items = all_items.where(Product.product_name.contains(search_query))

        for item in all_items:
            print('Product name: ', item.product_name)
        print('\n')
        

def item_search_menu():
    while True:
        print('*' * 25, 'SEARCH INVENTORY', '*' * 25)
        print('''
            To search by name press "0".
            To search by ID number press "1".
            To look at all current products type "ALL".
            To exit search menu press "Q" to quit.
        ''')
        user_input = input('Option Select: ')
        if user_input.lower() == '0':
            clear()
            search(input('Search by item name: '))
        elif user_input.lower() == '1':
            clear()
            id_search()
        elif user_input.lower() == 'all':
            clear()
            for item in Product.select():
                print('Product ID: ', item.id, '\t\t', 'Item name: ',item.product_name)
                
        elif user_input.lower() == 'q':
            clear()
            break
        else:
            clear()
            print('Please enter a valid option!\n')
                
def id_finder(search_query = None):
    item_id = Product.select()
    for item in item_id:
        if item.id == search_query:
            print('*' * 25, 'ID searched', '*' * 25)
            print('Product ID:', item.id, '\t', 'Product Name:', item.product_name)
            
def id_search():
    try:
        id_finder(int(input('Please enter any ID number or 0 to exit: ')))
    except ValueError:
        pass
        
def add_product_menu():
     while True:
        #clear()
        print('*' * 25, 'New Product Menu', '*' * 25)
        print('''
                To add a new product press 0
                To delete recently created product press 1
                To quit press "Q" to leave
        ''')
        user_input = input('Please enter a valid option: ')
        if user_input == '0':
            clear()
            add_product()
        elif user_input == '1':
            clear()
            delete_product()
        elif user_input.lower() == 'q':
            clear()
            break
    
def add_product():
    clear()
    while True:
        print('*' * 25,'New Product Menu','*' * 25)
        item_name = input('Enter item name: ')
        while True:
            try:
                item_stock = int(input('Enter the STOCK in whole numbers only: '))
                item_price = int(input('Enter the PRICE in whole numbers only: '))
                break
            except ValueError:
                print('!!!Please enter a whole number only!!!')
        date_stamp = ('{:%m/%d/%Y}'.format(datetime.datetime.now()))
        try:
            item_added = Product.create(product_name = item_name, product_quantity = item_stock, product_price = item_price, date_updated = date_stamp)
            item_added.save()
            
        except IntegrityError: # if it fails do nothing
            pass
        clear()
        print('!!!PRODUCT CREATED!!!')
        break
          
def delete_product():
    Product.delete().where(Product.product_name()).execute()
    
    
    
def db_backup():
    pass
    
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    csv_extractor()
    main_menu()
