from services.order_service import OrderService
from services.catalog_service import load_catalog
from storage import Storage
from models.cart import Cart
from services.menu_loader import main_menu, admin_menu, sort_menu
from models.catalog import Catalog
from models.admin import Admin

storage = Storage()
catalog = Catalog()
load_catalog(catalog, storage)
cart = Cart()
order_service = OrderService(storage)
admin = Admin(storage)

while True:
    main_menu()
    choice = input("Choose option: ")
    if choice == "1":  #show catalog
        print("\nCatalog of Shop:")
        print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
        for p in catalog.show_catalog():
            print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
    if choice == "2":  #add to cart
        try:
            pid = int(input("Enter ID of product: "))
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input!")
            print("Please enter correct data!")
            continue
        product = catalog.get_by_id(pid)
        if not product:
            print("Product not found in catalog!")
        elif cart.add(product, qty):
            print(f"Product {product.name} added to cart!")
        else:
            print("Can not add product to cart!")
    if choice == "3":  #show cart
        if not cart.items:
            print("Cart is empty!")
            continue
        print("\nCART items:")
        print(f"{'ID': <3}{'NAME': <12}{'Quantity': <10}")
        for p in cart.items:
            print(f"{p.product.id: <3}{p.product.name: <12}{p.qty: <10}")

    if choice == "4":  #remove from cart
        try:
            pid = int(input("Enter ID of product: "))
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input!")
            print("Please enter correct data!")
            continue
        product = catalog.get_by_id(pid)
        if not product:
            print("Product not found in catalog!")
            continue
        cart.remove(product.id, qty)

    if choice == "5":  #checkout
        order = order_service.checkout(cart, catalog)
        if not order:
            print("Can not checkout!")
        try:
            storage.save_orders(order)
            storage.save_products(catalog.all())
        except Exception as e:
            print(f"Error saving data: {e}")
        print("Order successfully completed!")

    if choice == "6":  #search
        find = catalog.find_by_name(input("Enter product name: "))
        if not find:
            print("Product not found!")
        else:
            print(f"Products found: {find}")

    if choice == "7":  #filter by price
        try:
            min_price = int(input("Enter minimum price: "))
            max_price = int(input("Enter maximum price: "))
        except ValueError:
            print("Invalid input!")
            print("Please enter correct data! Numbers only!")
            continue
        filtered = catalog.filter_by_price(min_price, max_price)
        print("Filtered products:")
        print(f"{'ID': <3}{'NAME': <12}{'COST': <10}")
        for p in filtered:
            print(f"{p.id: <3}{p.name: <12}{p.cost: <10}")

    if choice == "8":  #show orders
        orders = storage.load_orders()
        if not orders:
            print("No orders yet!")
            print("Please make some purchases!")
            continue
        print(f"Orders: {orders}")
    
    if choice == "9":  #admin menu
        while True:
            admin_menu()
            choice_admin = input("Choose option: ")
            if choice_admin == "0":
                break
            if choice_admin == "1":  #add product
                print("\nCurrent catalog:")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.show_catalog():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
                print("\nAdding new product")
                try:
                    pid = int(input("Enter the id of product"))
                    name = input("Enter product name: ")
                    price = float(input("Enter product price: "))
                    quantity = int(input("Enter product quantity: "))
                except ValueError:
                    print("Invalid input!")
                    print("Please enter correct data!")
                    continue
                x,msg = admin.add_product_adm(catalog,pid,name,price,quantity)
                print (msg)
            if choice_admin == "2":  #edit price
                print("\nCurrent catalog:")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.show_catalog():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
                print("\nEditing product price")
                try:
                    pid = int(input("Enter the id of product"))
                    price = float(input("Enter product price: "))
                except ValueError:
                    print("Invalid input!")
                    print("Please enter correct data!")
                    continue
                x,msg = admin.edit_price_adm(catalog,pid,price)
                print(msg)
            if choice_admin == "3": #edit qty
                print("\nCurrent catalog:")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.show_catalog():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
                print("\nEditing product quantity")
                try:
                    pid = int(input("Enter the id of product"))
                    qty = int(input("Enter product quantity: "))
                except ValueError:
                    print("Invalid input!")
                    continue
                x, msg = admin.edit_price_adm(catalog,pid,qty)
                print(msg)
            if choice_admin == "4":  #delete product
                print("\nCurrent catalog:")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.show_catalog():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
                try:
                    pid = int(input("Enter the id of product"))
                except ValueError:
                    print("Invalid input!")
                    continue
                x, msg = admin.delete_product_adm(catalog,pid)
                print(msg)
    if choice == "10":
        print("Sorting Catalog...")
        while True:
            sort_menu()
            choice_sort = input("Choose sorting method: ")
            if choice_sort == "0":
                break
            if choice_sort == "1": #sort price asc
                print("Sorting by price ascending...")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.sort_catalog_price_ascending():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
            if choice_sort == "2":  #sort price desc
                print("Sorting by price descending...")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.sort_catalog_price_descending():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
            if choice_sort == "3":  #sort name asc
                print("Sorting by name ascending...")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.sort_catalog_name_ascending():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")
            if choice_sort == "4":   #sort name desc
                print("Sorting by name descending...")
                print(f"{'ID': <3}{'NAME': <12}{'COST': <10}{'REMAINS': <10}")
                for p in catalog.sort_catalog_name_descending():
                    print(f"{p.id: <3}{p.name: <12}{p.cost: <10}{p.remains: <10}")

    if choice == "0":
        break