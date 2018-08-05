from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#####################################################################
class Customer(db.Model):
    """Customers of Kart."""

    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        """Provide a helpful representation."""

        return '<Customer customer_id={} first_name={}>'.format(
               self.customer_id, self.first_name)


class Product(db.Model):
    """Products."""

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(150))

    def __repr__(self):
        """Provide useful representation."""

        return '<Product product_id={} name={} cat_id={}>'.format(
               self.product_id, self.name)


class Cart(db.Model):
    """Customer's cart."""

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    customer = db.relationship('Customer', backref=db.backref('carts', order_by=cart_id))
    product = db.relationship('Product', backref=db.backref('carts', order_by=cart_id))

    def __repr__(self):
        """Provide a helpful representation."""

        return '<Cart cart_id={} product_id={} quantity={}>'.format(
                self.cart_id, self.product_id, self.quantity)


def example_data():
    """Data for testing."""

    customer = Customer(first_name='John',
                        last_name='Doe',
                        email='sp@y',
                        password='123',
                        phone='1234567891',
                        address='California'
                        )

    product = Product(name='potato')

    cart = Cart(customer_id=1,
                product_id=1,
                quantity=3)

    db.session.add(customer)
    db.session.add(product)
    db.session.add(cart)

    db.session.commit()


##############################################################################

def connect_to_db(app, db_uri='postgresql:///testdb'):
    """Connect the database to Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    connect_to_db(app)
    print("Connected to DB.")
