#this menu lets the user see what is in the current inventory until it is updated via database 
def view_inventory():
    clear()
    
    while True:

        print('*' * 25, '(INVENTORY MENU)', '*' * 25) 
        print('''
            Enter "A" to view all current inventory products
            Enter "S" to view all current stock available
            Enter "P"  to view all current inventory prices
            Enter "0" to exit inventory menu:
            ''')
        inventory_commands = input('Enter command: ')
        if inventory_commands.lower() == 'a':
            for item in Product.select():
                print('Date added:', '\t', 'Product name:')
                print(item.product_dates, '\t', item.product_names)
                
        elif inventory_commands.lower() == 's':
            for item in Product.select():
                print('Available Stock:', '\t\t', 'Product names:')
                print(item.product_quantity, '\t\t\t\t', item.product_names)
                
        elif inventory_commands.lower() == 'p':
            for item in Product.select():
                print('Current price:', '\t\t', 'Product names:')
                print(item.product_prices, '\t\t\t', item.product_names)
                
        elif inventory_commands.lower() == '0':
            print('\nLeaving inventory menu...\n')
            break
        else:
            print('Please enter a valid command')
            
            
#*****not finished*****            
def search_inventory(search_query = None):
    clear()
    while True:
        print('*' * 25, '(SEARCH MENU)', '*' * 25)
        print('''
            Search anything within the store.
            
                          OR
                        
            Press "0" to exit search menu.
        ''')
        item_lookup = input('Search items: ')
        items = Product.select()
        if search_query:
            items = items.where(Product.product_names.contains(search_query))
        for item in items:
            print(item.product_names)
        
#*****not finished*****
def edit_inventory():
    clear()
    while True:
        print('*' * 25, '(EDIT MENU)', '*' * 25)
        print('''
            Press "A" to add a product.
            Press "E" to edit a product.
            Press "D" to delete a product.
            
                        OR
            Press "0" to exit edit menu
        ''')
        
        edit_controls = input('Enter command: ')
        
        if edit_controls.lower() == 'a':
            #print('enter your entry. press CTRL+D when finished')
            #data = sys.stdin.read().strip()
            #if data:
                #if input('\nSave entry? [Yn] ').lower() != 'n':
                #Entry.create(content = data)
                #print('Saved successfully')
                pass
        elif edit_controls.lower() == 'e':
            pass
        elif edit_controls.lower() == 'd':
            pass
        elif edit_controls == '0':
            print('\nLeaving edit menu...\n\n')
            break
        else:
            print('\nPlease enter a valid command\n')
        
            

#creates the first menu the user sees and links the other menus and loops over them
def menu_interface():
    while True:
        print('*' * 25, '(STORE MENU)', '*' * 25)
        print('Please select an option below:')
        print('''
              Press "V" to view all store inventory.
              Press "S" to search for products.
              Press "E" to edit store inventory.
              Press "Q" to exit application.
              ''')
        user_input = input('Menu Select: ')
        
        if user_input.lower() == 'v':
            view_inventory()
        elif user_input.lower() == 's':
            search_inventory()
        elif user_input.lower() == 'e':
            edit_inventory()
        elif user_input.lower() == 'q':
            sys.exit('\nExiting application...\n')
        else:
            print('\nPlease enter a valid command!\n')

#makes sure file is not ran automatically        
if __name__ == '__main__':
    #connects the database and creates the tables and runs the main fuctions 
    db.connect()
    db.create_tables([Product], safe = True)
    menu_interface()
