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
                Press "V" to view product IDs.
                Press "A" to add a new product to the database.
                Press "B" to backup the database to a CSV file.
                Press "0" to quit the application.''')
                
            option_select = input('\nPlease select an option obove: ')
            if option_select.lower() == 'v':
                clear()
                item_search()
            elif option_select.lower() == 'a':
                clear()
            elif option_select.lower() == 'b':
                clear()
            elif option_select.lower() == '0':
                clear()
                sys.exit('Leaving application...')
            else:
                print('Please select a valid option!')

def search_menu(search_query = None):
    all_items = Product.select()
    print('*' * 25,'Item Searched','*' * 25)
    if search_query:
        all_items = all_items.where(Product.product_names.contains(search_query))
        for item in all_items:
            print('Product name: ', item.product_names, '-', 'Product ID: ', item.id)

def item_search():
    search_menu(input('Search by item name or product ID: '))    
    
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    csv_extractor()
    main_menu()
