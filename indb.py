from product import Product

def generate_products():
    list_products = []
    for x in range(10):
       p =  Product(name=f"Product { x+1 }", price = 4.90 * x)
       list_products.append(p)
    return list_products