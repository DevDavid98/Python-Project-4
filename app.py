from peewee import *
import datetime
import csv
import sys
import re
import os

# to-do list

# (TOP PRIORITY)
# Xfigure out how to save and update existing items with new data
# X how to delete items within DB
# xfigure out product_id

# (functionality)
# show stock of items
# show dates of items
# show price of items

# (finishing touches)
# backup whole database to a csv file
# documentation of code via doctext
# find errors
# xclean code
# turn in for grade

db = SqliteDatabase('inventory.db')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Product(Model):

    # product_id = AutoField()
    product_quantity = IntegerField(unique=True)
    product_price = IntegerField()
    date_updated = DateField()
    product_name = CharField(unique=True)

    class Meta:

        database = db


def csv_extractor():

    with open('inventory.csv', 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        next(file_reader)

        for item in file_reader:

            foods = item[0]
            food_cost = int(re.sub('[^0-9]', '', item[1]))
            item_stock = int(item[2])
            added_dates = item[3]

            try:
                inventory = Product.create(
                    product_name=foods,
                    product_quantity=item_stock,
                    product_price=food_cost,
                    date_updated=added_dates
                )

            # try to create the Product
            except IntegrityError:  # if it fails do nothing
                pass

            else:  # if it doesn't fail, save it
                inventory.save()


def main_menu():
    while True:

        print('Welcome to the store inventory')
        program_start = input('To start the program click "S" to start: ')

        if program_start.lower() == 's':
            break

        else:
            clear()
            print('*' * 25, 'Please enter a valid option!', '*' * 25, '\n')

    if program_start.lower() == 's':
        clear()

        print('*' * 25, 'Store Inventory', '*' * 25)

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
                db_backup()

            elif option_select.lower() == '0':
                clear()
                sys.exit('Leaving application...')

            else:
                print('Please select a valid option!')


def search(search_query=None):

    all_items = Product.select()

    print('*' * 25, 'Item Searched', '*' * 25)

    if search_query:

        all_items = all_items.where(
            Product.product_name.contains(search_query)
        )

        for item in all_items:

            print('Product Name:\n',
                  item.product_name,
                  '\nProduct Stock:\n',
                  item.product_quantity,
                  '\nProduct Price:\n',
                  item.product_price,
                  '\nLast Updated:\n',
                  item.date_updated
                )

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

                print(
                    'Product ID: ', item.id, '\n'
                    'Product name: ', item.product_name, '\n',
                    'Product stock: ', item.product_quantity, '\n',
                    'Product price: ', item.product_price, '\n',
                    'Date updated: ', item.date_updated, '\n\n'
                )

        elif user_input.lower() == 'q':
            clear()
            break

        else:
            clear()
            print('Please enter a valid option!\n')


def id_finder(search_query=None):
    item_id = Product.select()

    for item in item_id:

        if item.id == search_query:

            print('*' * 25, 'ID searched', '*' * 25)
            print(
                'Product ID:\n', 
                item.id,
                '\nProduct Name:\n',
                item.product_name,
                '\nProduct Stock:\n',
                item.product_quantity,
                '\nProduct Price:\n',
                item.product_price,
                '\nLast Updated:\n',
                item.date_updated
            )


def id_search():
    try:
        id_finder(int(input('Please enter any ID number or 0 to exit: ')))

    except ValueError:
        pass


def add_product_menu():

    while True:

        clear()

        print('*' * 25, 'New Product Menu', '*' * 25)
        print('''
            To add a new product press 0
            To update any product press 1
            To delete recently created product press 2
            To quit press "Q" to leave  
        ''')

        user_input = input('Please enter a valid option: ')

        if user_input == '0':
            clear()
            add_product()
    
        elif user_input == '1':
            clear()
            update_inventory()

        elif user_input == '2':
            clear()
            delete_product()

        elif user_input.lower() == 'q':
            clear()
            break


def add_product():
    current_inventory = Product.select()
    clear()

    while True:
        print('*' * 25, 'New Product Menu', '*' * 25)

        #current_inventory = Product.select()

        print('ALL ITEMS IN INVENTORY:')
        for item in current_inventory:
            print(item.product_name)

        item_name = input('\nEnter new product name: ')
        print('Product Created...\n')

        while True:
            try:
                item_stock = int(input(
                        'Enter product stock: '
                    ))

            except ValueError:
                print('!!!Please enter a whole number only!!!')

            break
            
        item_price = input(
            'Enter product price: '
            )
        price_converter = int(re.sub('[^0-9]', '', item_price))

        date_stamp = ('{:%m/%d/%Y}'.format(datetime.datetime.now()))

        try:
            item_added = Product.create(
            product_name=item_name,
            product_quantity=item_stock,
            product_price=price_converter,
            date_updated=date_stamp
            )

            item_added.save()
            item_added.update()

        except IntegrityError:  # if it fails do nothing
            pass
        
        break

def delete_product():

    clear()

    print('*' * 25, 'Delete product Menu', '*' * 25)

    while True:
        all_inventory = Product.select()
        print('''
            To delete by product ID press 'I'.
            To exit press 'E'.
        ''')

        menu_select = input('Enter valid option: ')
        print('\n')

        if menu_select.lower() == 'i':

            print('ALL CURRENT INVENTORY:')

            for product in all_inventory:
                print('ID:',product.id, 'Product Name:', product.product_name)

            while True:
                try:
                    deleted_id = int(input(
                        'To delete an item(s) please type the product ID number or 0 to cancel: '
                    ))
                    Product.delete().where(Product.id == deleted_id).execute()
                    print('Product Deleted...')
                    if deleted_id == 0:
                        
                        break
                except ValueError:
                    print('Please enter a product ID.')

        elif menu_select.lower() == 'e':
            break
        
        else:
            print('Please enter a valid option!')


def db_backup():

    product_table = Product.select()

    with open('Inventory Backup.csv', 'w') as inventory_table:

        product_writer = csv.writer(inventory_table,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL,
                                   )

        product_table = Product.select()
        header = ['Product ID', 'Product Name', 'Product Quantity', 'Product Price', 'Date Updated']
        product_writer.writerow(header)
        for item in product_table:
            product_writer.writerow([item.id,item.product_name,
                                     item.product_quantity,
                                     item.product_price,
                                     item.date_updated]
                                   )
    while True:
        user_backup = input('Would you like to view the recently saved database Y/N?: ')
        
        if user_backup.lower() == 'y':
            with open('Inventory Backup.csv', 'r') as csv_file:
                file_reader = csv.reader(csv_file)
                for item in file_reader:
                    print(item)
            break

        elif user_backup.lower() == 'n':
            print('Returning to main menu...')
            break

        else:
            print('Please enter a valid option')
        

def update_inventory():
    pass
    #current_inventory = Product.select()
    #while True:
        #for item in current_inventory:
            #print(
                    #'Product ID:\n', 
                    #item.id,
                    #'\nProduct Name:\n',
                    #item.product_name,
                    #'\nProduct Stock:\n',
                    #item.product_quantity,
                    #'\nProduct Price:\n',
                    #item.product_price,
                    #'\nLast Updated:\n',
                    #item.date_updated
                #)
        #try:
            #where_update = str(input('Please type the item you would like to update: '))
            #update_stock = int(input('Please enter the desired quantity: '))
            #update_price = input('Please enter the desired price: ')
            #price_converter = int(re.sub('[^0-9]', '', update_price))
            #update_date = ('{:%m/%d/%Y}'.format(datetime.datetime.now()))

        #except ValueError:
            #print('Please enter a valid valid value')

        #updated = (Product
         #.update({Product.product_quantity==update_stock})
         #.where(Product.product_name == 'where_update'))


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    csv_extractor()
    main_menu()
