from peewee import *
import datetime
import csv
import sys
import re


#create database name and db
db = SqliteDatabase('inventory.db')


class Product(Model):
    #product_names = CharField(unique = True)
    product_quantity = IntegerField(unique = True)
    class Meta():
        database = db


#def view_all_inventory():
#    all_products = inventory[3]
#    try:
#        product_records = Product.create(product_names = all_products)
#        product_records.save()
#    except IntegrityError:
#        records = Product.get(product_names = all_products)
        
                
def all_product_stock():
    for the_stock in inventory[0:1]:
        for item in the_stock.values():
            for all_quantities in item:
                product_stock = Product.create(product_quantity = all_quantities)
                product_stock.save()

def all_product_prices():
    pass
def all_product_dates():
    pass
def all_product_ids():
    pass
def delete_products():
    pass
def add_products():
    print('Hello, what item would you like to add?')
    #add name
    #how many
    #create date added



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
    for items in inventory:
        all_stock = int(items[2])
        all_products = items[0]
        dates = items[3]
        price = int(re.sub('[^0-9]','',items[1]))

        all_inventory.append(all_products)
        product_quantity.append(all_stock)
        date_updated.append(dates)
        product_price.append(price)
    
    #has all information ready to use  

    inventory = [
        {'quantity': product_quantity},
        {'price': product_price},
        {'updated': date_updated},
        {'all_products': all_inventory}
    ]
    
           
#def clean_data():
#    for dict in inventory:
#        for value in dict.values():
#            print('\n')
#            for item in value:
#                print(item)
#clean_data()









#for price in product_price:
#    print(price)
#print('\n')
#for item in all_inventory:
#    print(item)  
#print('\n')
#for number in product_quantity:
#    print(number)
#print('\n')
#for date in date_updated:
#    print(date)
    
    
    


if __name__ == '__main__':
    #connects and creates the database and table if it was not created
    db.connect()
    db.create_tables([Product], safe = True)
    #view_all_inventory()
    all_product_stock()
