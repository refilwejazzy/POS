class Sale:
    def __init__(self):
        self.total_sale = 0.0


class Table:
    def __init__(self, table_num):
        self.table_num = table_num
        self.server = None
        self.customers = 0
        self.orders = []

    def assign_server(self, server):
        self.server = server

    def add_customers(self, count):
        self.customers = count

    def add_order(self, order):
        self.orders.append(order)

    def prepare_bill(self):
        total = sum(order.price * order.quantity for order in self.orders)
        bill = f"Table: {self.table_num}\n"
        bill += "----------------------\n"
        for order in self.orders:
            bill += f"{order.name} x {order.quantity}: R{order.price * order.quantity}\n"
        bill += "----------------------\n"
        bill += f"Total: R{total}\n"
        return bill, total

    def clear_table(self):
        self.server = None
        self.customers = 0
        self.orders = []


class Order:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


def read_login_cred(file_name):
    credentials = {}
    with open(file_name, 'r') as file:
        for line in file:
            username, passwrd = line.strip().split(',')
            credentials[username] = passwrd
    return credentials


def read_menu(file_name):
    menu = {}
    with open(file_name, 'r') as file:
        for line in file:
            item_name, item_price = line.strip().split(',')
            menu[item_name] = float(item_price)
    return menu


def display_menu():
    print("Main Menu:")
    print("1. Assign Table")
    print("2. Change Customers")
    print("3. Add to Order")
    print("4. Prepare Bill")
    print("5. Complete Sale")
    print("6. Cash Up")
    print("0. Log Out")


def assign_table(current_server, table_list):
    print("Available tables:")
    available_tables = [table for table in table_list if table.server is None]
    for table in available_tables:
        print(f"Table {table.table_num}")
    table_num = int(input("Enter the table number: "))
    table = next((table for table in table_list if table.table_num == table_num), None)
    if table and table.server is None:
        table.assign_server(current_server)
        choice = input("Do you want to add customers to the table? (y/n): ")
        if choice.lower() == "y":
            count = int(input("Enter the number of customers: "))
            table.add_customers(count)
        print("Table assigned successfully!")
    else:
        print("Invalid table number or the table is already assigned.")


def change_customers(current_server, table_list):
    print("Tables assigned to you:")
    assigned_tables = [table for table in table_list if table.server == current_server]
    for table in assigned_tables:
        print(f"Table {table.table_num}")
    table_num = int(input("Enter the table number: "))
    table = next((table for table in table_list if table.table_num == table_num and table.server == current_server), None)
    if table:
        count = int(input("Enter the new number of customers: "))
        table.add_customers(count)
        print("Number of customers changed successfully!")
    else:
        print("Invalid table number or the table is not assigned to you.")


def add_to_order(current_server, table_list, menu_items):
    print("Tables assigned to you:")
    assigned_tables = [table for table in table_list if table.server == current_server]
    for table in assigned_tables:
        print(f"Table {table.table_num}")
    table_num = int(input("Enter the table number: "))
    table = next((table for table in table_list if table.table_num == table_num and table.server == current_server), None)
    if table:
        print("Menu:")
        for item_name, item_price in menu_items.items():
            print(f"{item_name}: R{item_price}")
        item_name = input("Enter the name of the item: ")
        if item_name in menu_items:
            item_price = menu_items[item_name]
            item_quantity = int(input("Enter the quantity: "))
            order = Order(item_name, item_price, item_quantity)
            table.add_order(order)
            print("Order added successfully!")
        else:
            print("Invalid item name.")
    else:
        print("Invalid table number or the table is not assigned to you.")


def prepare_bill(current_server, table_list):
    print("Tables assigned to you:")
    assigned_tables = [table for table in table_list if table.server == current_server]
    for table in assigned_tables:
        print(f"Table {table.table_num}")
    table_num = int(input("Enter the table number: "))
    table = next((table for table in table_list if table.table_num == table_num and table.server == current_server), None)
    if table:
        bill, total = table.prepare_bill()
        print("Bill:")
        print(bill)
        file_name = input("Enter the file name to save the bill: ")
        with open(file_name, 'w') as file:
            file.write(bill)
        print("Bill successfully prepared!")
        return total
    else:
        print("Invalid table number or the table is not assigned to you.")
        return 0.0


def complete_sale(current_server, table_list, current_sale):
    print("Tables assigned to you:")
    assigned_tables = [table for table in table_list if table.server == current_server]
    for table in assigned_tables:
        print(f"Table {table.table_num}")
    table_num = int(input("Enter the table number: "))
    table = next((table for table in table_list if table.table_num == table_num and table.server == current_server), None)
    if table:
        if len(table.orders) > 0:
            total = prepare_bill(current_server, table_list)
            current_sale.total_sale += total
            table.clear_table()
            print("Sale completed successfully!")
        else:
            print("No orders found for the table.")
    else:
        print("Invalid table number or the table is not assigned to you.")


def cash_up(current_sale):
    print("Total sales: R", current_sale.total_sale)
    choice = input("Do you want to clear the daily total? (y/n): ")
    if choice.lower() == "y":
        current_sale.total_sale = 0.0
        print("Daily total cleared.")


def point_of_sale():
    login_file = "Login.txt"
    menu_file = "Menu.txt"
    login_cred = read_login_cred(login_file)
    menu_items = read_menu(menu_file)
    table_list = [Table(i + 1) for i in range(6)]
    current_sale = Sale()
    current_server = input("Username: ")
    passwrd = input("passwrd: ")
    if current_server in login_cred and login_cred[current_server] == passwrd:
        print("Login successful!")
        while True:
            display_menu()
            choice = int(input("Enter your choice: "))
            if choice == 1:
                assign_table(current_server, table_list)
            elif choice == 2:
                change_customers(current_server, table_list)
            elif choice == 3:
                add_to_order(current_server, table_list, menu_items)
            elif choice == 4:
                prepare_bill(current_server, table_list)
            elif choice == 5:
                complete_sale(current_server, table_list, current_sale)
            elif choice == 6:
                cash_up(current_sale)
            elif choice == 0:
                print("Logged out successfully!")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid username or passwrd. Login failed.")


point_of_sale()