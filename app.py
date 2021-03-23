from peewee import *
import datetime
import csv
import sys
import re
import os


db = SqliteDatabase('inventory.db')
class Product(Model):
    product_id = IntegerField(primary_key = True)
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
                inventory = Product.create(product_id, product_names = foods, product_quantity = item_stock, product_price = food_cost, date_updated = added_dates)
            # try to create the Product
            except IntegrityError: # if it fails do nothing
                pass
            else: #if it doesn't fail, save it
                inventory.save()
#def id_viewer():
    #for item in Product.select():
        #print(item.product_id,'\n')
        #print(item.product_price)

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe = True)
    csv_extractor()
    #id_viewer()
#new version of app.py
