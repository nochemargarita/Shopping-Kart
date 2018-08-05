from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import connect_to_db, db, Customer, Product, Cart
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_debugtoolbar import DebugToolbarExtension
from kart import Kart
import json

app = Flask(__name__)

app.secret_key = "ABC"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Return homepage."""
    if session.get('email'):
        return redirect('/shop')

    else:
        return render_template('homepage.html')


@app.route('/signup', methods=['POST'])
def sign_up():
    """Process sign-up using POST request."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    address = request.form['address']

    hashed_password = generate_password_hash(password)

    already_customer = db.session.query(Customer).filter(Customer.email == email).first()

    if already_customer:
        flash('Email already taken.')
        return redirect('/')
    else:
        flash('You can now start shopping.')
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=hashed_password,
                            phone=phone,
                            address=address)

        db.session.add(customer)
        db.session.commit()
        session['email'] = email

    return render_template('shop.html')


@app.route('/login', methods=['POST'])
def login():
    """Process customer's entered email and password and confirm."""

    email = request.form['email']
    password = request.form['password']

    already_customer = db.session.query(Customer).filter(Customer.email == email).first()

    if already_customer:
        checked_hashed = check_password_hash(already_customer.password, password)
        if checked_hashed:
            name = already_customer.first_name.capitalize()
            flash('Welcome to Kart, {}!'.format(name))
            session['email'] = email
            return render_template('shop.html')
        else:
            flash('Your password didn\'t match the email')
            return redirect('/')

    else:
        flash('Please check your email and password.')
        return redirect('/')


@app.route('/logout')
def logout():
    """Clear customer from session."""

    session.clear()

    return redirect('/')


@app.route('/shop')
def shop():
    """Search for products/items."""
    if session.get('email'):
        return render_template('shop.html')
    else:
        return redirect('/')


@app.route('/suggestions')
def get_products():
    """get all product suggestions from db."""
    products = db.session.query(Product).all()
    product_details = {}

    for product in products:
        product_details[product.product_id] = product.name

    return jsonify(product_details)


@app.route('/kartItem', methods=['POST'])
def cart_product():
    email = session.get('email')

    if email:
        chosen = request.form.get('data')
        print chosen
        for name, quantity in json.loads(chosen).iteritems():
            product = Kart()
            product.add_to_cart(email, name, quantity)
            product.update_kart(email, name, quantity)

        return 'See you next time! Your items will wait for you.'
    else:
        return redirect('/')


@app.route('/kart')
def get_cart_product():
    """Get all the product from the cart associated with the customer."""
    email = session.get('email')
    if email:
        customer = db.session.query(Customer).filter(Customer.email == email).first()

        products = {}

        cart = db.session.query(Cart).filter(Cart.customer_id == customer.customer_id).all()

        for product in cart:
            products[product.product.name] = product.quantity

        return jsonify(products)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.run(host='0.0.0.0')
