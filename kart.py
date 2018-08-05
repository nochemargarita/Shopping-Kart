from model import connect_to_db, db, Customer, Product, Cart


class Kart(object):

    def add_to_cart(self, email, name, quantity):
        """Adds the product to db."""
        self.name = name
        self.quantity = quantity
        self.email = email

        customer = db.session.query(Customer).filter(Customer.email == self.email).first()
        product = db.session.query(Product).filter(Product.name == self.name).first()

        cart = Cart(customer_id=customer.customer_id, product_id=product.product_id, quantity=quantity)

        db.session.add(cart)
        db.session.commit()

    


if __name__ == "__main__":
    connect_to_db(app)
    Kart()
