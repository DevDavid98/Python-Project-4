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
            print('Item:')
            print(foods)
            print('Item Stock:')
            print(item_stock)
            print('Item Cost:')
            print(food_cost)
            print('Date Added:')
            print(added_dates)
            try:
                inventory = Product.create(product_names = foods, product_quantity = item_stock, product_prices = food_cost, product_dates = added_dates)
            # try to create the Product
            except IntegrityError: # if it fails do nothing
                pass
            else: #if it doesn't fail, save it
                inventory.save()
def view_all():
    all_inventory()
                
def menu_interface():
    while True:
        print('*' * 25, 'Store Inventory', '*' * 25)
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
            pass
        elif user_input.lower() == 'e':
            pass
        elif user_input.lower() == 'q':
            sys.exit('\nExiting application...\n')
    

        
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    menu_interface()
