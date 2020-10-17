from peewee import *
import datetime
import csv
import sys
import re





#create database name and db
db = SqliteDatabase('inventory.db')
class Product(Model):
    product_names = CharField()
    product_quantities = IntegerField()
    product_prices = IntegerField()
    product_dates = DateTimeField()
    product_id = primary_key()
    class Meta():
        database = db
    
def all_product_names():
    pass
def all_product_prices():
    pass
def all_product_dates():
    pass
def all_product_ids():
    pass
def delete_products():
    pass
def add_products():
    pass
def edit_products():
    pass


#creates main menu
def main_menu():
    print('-' * 44)
    print('Welcome to the story inventory main menu.')
    print('Please select a menu option to begin')
    print('-' * 44)
    print('''
    Select "V" to view all inventory
    Select "E" to edit inventory
    Select "S" to search inventory
    Select "Q" to quit the application
    ''')
    print('-' * 44)
    while True:
        user_option = input('Menu Select: ')
        
        if user_option.lower() == 'v':
            pass
        elif user_option.lower() == 'e':
            pass
        elif user_option.lower() == 's':
            pass
        elif user_option.lower() == 'q':
            sys.exit('Closing application.')
        else:
            print('INVALID OPTION')
            print('Please enter valid a option')


#gets csv information
#stores csv info as divt within list
with open('inventory.csv', 'r') as csv_file:
    inventory = csv.reader(csv_file)
    next(inventory)
    
    #creates list for every section of csv file
    product_quantity = []
    product_price = []
    date_updated = []
    all_inventory = []
    
    #enters for loop and cleans the csv data 
    for line in inventory:
        product_quantity.append(int(line[2]))
        all_inventory.append(line[0])
        product_price.append(int(re.sub('[^0-9]','',line[1])))
        date_updated.append(line[3])
    
    #has all information ready to use    
    inventory = [
        {'quantity': product_quantity},
        {'price': product_price},
        {'updated': date_updated},
        {'all_products': all_inventory}
    ]

if __name__ == '__main__':
    #connects and creates the database and table if it was not created
    db.connect()
    db.create_tables([Product], safe = True)
    all_product_names()
