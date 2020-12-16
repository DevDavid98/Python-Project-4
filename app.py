from peewee import *
import datetime
import csv
import sys
import re

db = SqliteDatabase('inventory.db')
class Product(Model):
    product_quantity = IntegerField()
    product_prices = IntegerField()
    product_names = CharField()
    class Meta():
        database = db
        
def add_inventory():
    with open('inventory.csv', 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        next(file_reader)
        for item in file_reader:
            foods = item[0]
            food_cost = int(re.sub('[^0-9]','',item[1]))
            item_stock = int(item[2])
            added_dates = item[3]

            add_data = Product.create(product_quantity = item_stock, product_prices = food_cost, product_names = foods)
            add_data.save()
            #food_data = Product.get(product_quantity = item_stock, product_prices = food_cost, product_names = foods)
                

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    add_inventory()
