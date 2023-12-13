"""
shop.py
Implements:
- Listing products
- Buying products
- Searching products
- Saving and loading inventory
"""

class Product:
    def __init__(self, name, qty, price):
        self.name = name
        self.qty = qty
        self.price = price 

    def __str__(self):
        return "[{:02}x] {} ({} each)".format(self.qty, self.name, self.price)
    
class Inventory:
    def __init__(self):
        self.products = {}

    # Loads inventory from a CSV file
    def load_inventory(self, fname):
        with open(fname, 'r') as f:
            for ix, l in enumerate(f):
                if ix > 0:
                    pid, name, qty, price = l.strip().split(',')
                    p = Product(name=name, qty=int(qty), price=int(price))
                    self.products[pid] = p
                    
    # Prints all available products
    def print_inventory(self):
        print("== PRODUCTS ==")
        for pid in self.products.keys():
            p = self.products[pid]
            print("{} {}".format(pid, p))

    # Gets an item based on PID and qty
    def get_item(self, pid, qty):
        if pid in self.products.keys():
            if self.products[pid].qty >= qty:
                # If the product exists, we clone the product then adjust qty
                product = self.products[pid]
                new_p = Product(name=product.name, qty=qty, price=product.price)
                
                self.products[pid].qty -= qty 
                return new_p
            
            else:
                return None
            
        else:
            return None
        
    # Returns an item to the inventory
    def set_item(self, pid, qty):
        self.products[pid].qty += qty

class Cart:
    def __init__(self):
        self.products = {}

    # Shows the currently added cart items
    def show_cart(self):
        print("== CART == ")
        for pid in self.products.keys():
            p = self.products[pid]
            print("{} {}".format(pid, p))

    # Adds item to cart based on pid
    def add_to_cart(self, inventory, pid, qty):
        p = inventory.get_item(pid, qty)
        if p is not None:
            self.products[pid] = p
            print("Added product:", p)
        else:
            print("Invalid Product ID or not enough inventory.")

    # Removes an item from the cart
    def remove_from_cart(self, inventory, pid, qty):
        if pid in self.products.keys():
            if self.products[pid].qty >= qty:
                print("Returning {}x of product {}".format(qty, self.products[pid]))
            
                # Return the qty to the inventory and reduce the quantity in cart
                inventory.set_item(pid, qty)
                self.products[pid].qty -= qty

                if self.products[pid].qty == 0:
                    del self.products[pid]
            else:
                print("Too much product quantity selected")
        else:
            print("Product with ID {} does not exist in cart".format(pid))

    # Initiates checkout
    def checkout(self):
        self.show_cart()
        total = 0
        for pid in self.products.keys():
            p = self.products[pid]
            total += p.price * p.qty
        print("Checkout total: {}".format(total))
        self.products = {}

if __name__ == '__main__':
    inventory = Inventory()
    inventory.load_inventory('inventory.csv')
    cart = Cart()

    while True:
        print("\nInventory System")
        print("[1] View Inventory\n[2] Add to Cart\n[3] Remove from Cart\n[4] View Cart\n[5] Checkout\n[6] Quit")
        choice = int(input("Enter choice: ").strip())
        print()

        if choice == 1:
            inventory.print_inventory()

        elif choice == 2:
            pid = input("Enter product ID: ").strip()
            qty = int(input("Enter quantity: ").strip())
            cart.add_to_cart(inventory, pid, qty)

        elif choice == 3:
            pid = input("Enter product ID: ").strip()
            qty = int(input("Enter quantity: ").strip())
            cart.remove_from_cart(inventory, pid, qty)

        elif choice == 4:
            cart.show_cart()

        elif choice == 5:
            cart.checkout()

        elif choice == 6:
            break

        print()
