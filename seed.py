from model import connect_to_db, db, Customer, Product
from server import app
import json


def products_to_db(filename):
    """Reads the items.json file and stores all the items in the kart database."""

    with open(filename, 'r') as filename:
        for item in json.load(filename):
            product = Product(name=item)

            db.session.add(product)

    print 'Now committing!'
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    products_to_db('items.json')
