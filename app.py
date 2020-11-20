from peewee import *
import datetime
import csv
import sys
import re

db = SqliteDatabase('inventory.db')
class Product(Model):
    product_quantity = IntegerField(unique = True)
    product_prices = IntegerField(unique = True)
    product_names = CharField(unique = True)
    class Meta():
        database = db
food_names = []
food_price = []
food_stock = []
dates_added = []

with open('inventory.csv', 'r') as csv_file:
    file_reader = csv.reader(csv_file)
    next(file_reader)
    for item in file_reader:
        foods = item[0]
        food_cost = int(re.sub('[^0-9]','',item[1]))
        item_stock = int(item[2])
        added_dates = item[3]

        food_names.append(foods)    
        food_price.append(food_cost)
        food_stock.append(item_stock)
        dates_added.append(added_dates)
        


inventory = [
    {'items': food_names},
    {'price': food_price},
    {'stock': food_stock},
    {'dates': dates_added}
]


def add_foods():
    for key in inventory:
        try:
            Product.create(product_quantity = key['stock'], product_prices = key['price'], product_names = key['items'])
        except IntegrityError:
            added_inventory = Product.get(product_quantity = key['stock'], product_prices = key['price'], product_names = key['items'])
            added_invewntory.save()
            
    
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    add_foods()
