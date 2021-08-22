# Import all modules for this application
from peewee import *
import datetime
import csv
import sys
import re
import os

# Creates the database called inventory
db = SqliteDatabase('inventory.db')


# Function ability: Clears all items in console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Only model contains all the essential parts of the db and data types
class Product(Model):

    # product_id = AutoField()
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()
    product_name = CharField(unique=True)

    class Meta:

        database = db


# Grabs all items within the given CSV file
def csv_extractor():

    with open('inventory.csv', 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        next(file_reader)

        for item in file_reader:

            foods = item[0]
            food_cost = int(re.sub('[^0-9]', '', item[1]))
            item_stock = int(item[2])
            added_dates = datetime.datetime.strptime(item[3], '%m/%d/%Y').date()

            try:
                inventory = Product.create(
                    product_name=foods,
                    product_quantity=item_stock,
                    product_price=food_cost,
                    date_updated=added_dates
                )

            except IntegrityError:
                pass

            else:
                inventory.save()


# Creates the main menu
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
            clear()
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


# Creates a search query to find IDs in the database
def search(search_query=None):

    all_items = Product.select()

    print('*' * 25, 'Item Searched', '*' * 25)

    if search_query:

        all_items = all_items.where(
            Product.product_name.contains(search_query)
        )

        for item in all_items:

            print(
                  'Product Name:\n',
                  item.product_name,
                  '\nProduct Stock:\n',
                  item.product_quantity,
                  '\nProduct Price:\n',
                  item.product_price,
                  '\nLast Updated:\n',
                  item.date_updated
                 )

        print('\n')


# Creates a search menu for user and shows all items in database
def item_search_menu():

    while True:

        print('*' * 25, 'SEARCH INVENTORY', '*' * 25)
        print('''
            To search by name press "0".
            To search by ID number press "1".
            To look at all current products type "ALL".
            To exit search menu press "Q".
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


# Searches IDs within the model with the search query function called "Search"
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


# Adds a loop for the ID search option
def id_search():
    while True:
        user_choice = input('Would you like to ID search [Y/N]?: ')
        if user_choice.lower() == 'y':
            try:
                id_finder(int(input('Please enter any ID number: ')))
            except ValueError:
                print('Please enter a valid ID number')
        elif user_choice.lower() == 'n':
            break
            clear()


# Adds another menu to the main menu
def add_product_menu():

    while True:

        clear()

        print('*' * 25, 'New Product Menu', '*' * 25)
        print('''
            To add a new product press "0".
            To update any product press "1".
            To delete any product press "2".
            To exit the New Product Menu press "Q".
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


# Adds new products to the model
def add_product():
    clear()
    current_inventory = Product.select()

    while True:
        print('*' * 25, 'New Product Menu', '*' * 25)

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
                break

            except ValueError:
                print('Please enter a whole number only.')
        while True:
            try:
                item_price = float(input(
                    'Enter product price: '
                    ))
                price_converter = item_price * 100
                break

            except ValueError:
                print('Please enter a valid price ex:(1.50, 150, .10)')

        date_stamp = datetime.datetime.now()

        try:
            item_added = Product.create(
                product_name=item_name,
                product_quantity=item_stock,
                product_price=price_converter,
                date_updated=date_stamp
            )
            item_added.save()

        except IntegrityError:
            pass

        break


# Deletes any item in the model via ID
def delete_product():

    clear()

    print('*' * 25, 'Delete product Menu', '*' * 25)

    while True:
        all_inventory = Product.select()
        print('''
            To delete by product ID press "1".
            To exit Delete Product Menu press "0".
        ''')

        try:
            menu_select = int(input('Enter valid option: '))
            print('\n')
        
            if menu_select == 1:

                print('ALL CURRENT INVENTORY:')
    
                for product in all_inventory:
                    print('ID:', product.id, 'Product Name:', product.product_name)
    
                while True:
                    try:
                        deleted_id = int(input(
                            'To delete an item please type the product ID number or 0 to cancel: '
                            ))
    
                        if deleted_id:
                            Product.delete().where(Product.id == deleted_id).execute()
                            print('Product Deleted...')
    
                        elif deleted_id == 0:
                            break
                        
    
                    except ValueError:
                        print('Please enter a product ID.')

            elif menu_select == 0:
                break
            else:
                print('Please enter "1" or "0".')
        except ValueError:
            print('Please enter "1" or "0".')

            


# Backups the database and shows the database to the user if needed
def db_backup():

    product_table = Product.select()

    with open('Inventory Backup.csv', 'w') as inventory_table:

        product_writer = csv.writer(
                inventory_table,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,)

        product_table = Product.select()
        header = [
            'Product ID',
            'Product Name',
            'Product Quantity',
            'Product Price',
            'Date Updated'
        ]
        product_writer.writerow(header)
        for item in product_table:
            product_writer.writerow([
                    item.id,
                    item.product_name,
                    item.product_quantity,
                    item.product_price,
                    item.date_updated
                    ])
    while True:
        user_backup = input('Would you like to view the recently saved database Y/N?: ')

        if user_backup.lower() == 'y':
            with open('Inventory Backup.csv', 'r') as csv_file:
                file_reader = csv.reader(csv_file)
                for item in file_reader:
                    print(item)
        elif user_backup.lower() == 'n':
            print('Returning to main menu...')
            break

        else:
            print('Please enter a valid option')


# Updates any item in database
def update_inventory():
    all_inventory = Product.select()
    while True:
        try:
            user_input = int(input('To update product press "1" or "0" to cancel: '))
            if user_input ==  1:
                print('ALL CURRENT INVENTORY:')
                for item in all_inventory:
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
                        item.date_updated,
                        '\n\n'
                    )
                while True:
                    try:
                        update_id = int(input('Enter the ID number to update item or press "0" to leave: '))
                        print('\n\n')
                        break
                    except ValueError:
                        print('Please enter a whole number')
                if update_id == 0:
                    break

                while True:
                    try:
                        new_product_quantity = int(input('Update the current stock of product number {}: '.format(update_id)))
                        print('\n\n')
                        break
                    except ValueError:
                        print('Please enter a whole number')
                        
                while True:
                    try:
                        new_product_price = float(input('Update current product price: '))
                        price_convert = new_product_price * 100
                        print('\n\n')
                        break
                    except ValueError:
                        print('Please enter a valid price ex:(1.50, 150, .10)')
                           
                new_date_stamp = datetime.datetime.now()
                quantity = Product.update(product_quantity = new_product_quantity).where(Product.id == update_id)
                price = Product.update(product_price = price_convert).where(Product.id == update_id)
                date = Product.update(date_updated = new_date_stamp).where(Product.id == update_id)
    
                quantity.execute()
                price.execute()
                date.execute()
            elif user_input == 0:
                break
        except ValueError:
            print('Please enter a whole number!')


# Makes sure file doesnt start when imported if i remember...
if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    csv_extractor()
    main_menu()
