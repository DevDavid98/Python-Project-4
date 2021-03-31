from peewee import *
import datetime
import csv
import sys
import re
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

db = SqliteDatabase('inventory.db')
class Product(Model):
    #product_id = IntegerField(unique = True, primary_key = True)
    product_quantity = IntegerField(unique = True)
    product_price = IntegerField(unique = True)
    date_updated = DateField(unique = True)
    product_names = CharField(unique = True)
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
                inventory = Product.create(product_names = foods, product_quantity = item_stock, product_price = food_cost, date_updated = added_dates)
            # try to create the Product
            except IntegrityError: # if it fails do nothing
                pass
            else: #if it doesn't fail, save it
                inventory.save()

def main_menu():
    print('Welcome to the store inventory')
    program_start = input('To start the program click "S" to start: ')
    if program_start.lower() == 's':
        clear()
        print('*' * 25,'Store Inventory', '*' * 25)
        while True:
            print('''Main Menu:
                Press "V" to view product information.
                Press "A" to add a new product to the database.
                Press "B" to backup the database to a CSV file.
                Press "0" to quit the application.''')
                
            option_select = input('\nPlease select an option obove: ')
            if option_select.lower() == 'v':
                clear()
                item_search_menu()
            elif option_select.lower() == 'a':
                clear()
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
        all_items = all_items.where(Product.product_names.contains(search_query))

        for item in all_items:
            print('Product name: ', item.product_names)
        print('\n')
        
        



def item_search_menu():
    while True:
        print('*' * 25, 'SEARCH INVENTORY', '*' * 25)
        print('''
            To search by name press "0".
            To search by ID number press "1".
            To look at all current products type in "ALL".
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
                print('Product ID: ', item.id, '\t\t', 'Item name: ',item.product_names)
                
        elif user_input.lower() == 'q':
            clear()
            break
        else:
            clear()
            print('Please enter a valid option!\n')
                
def id_finder(search_query):
    #I need help I cant figure out the logic to search for the product ID
    #I can search the items by name and i can get the item ID but i cant search it.
    #I also can not implement this code below without crashing the whole program what data do i pair it with(located in the Product Model)?
    #product_id = IntegerField(unique = True, primary_key = True)
    #I noticed it already creates the product_ids without the line above but the project wants me to use it.
    #could you please give me a video or examples because I learn through example and implementing it in my own way and style!
    pass
    
    
    
def id_search():
    id_finder(input('Search item ID: '))
        
        

        
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    csv_extractor()
    main_menu()
