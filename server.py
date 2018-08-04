from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import connect_to_db, db, Customer, Product, Cart
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Return homepage."""
    if session.get('email'):
        return redirect('/kart')

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

    return render_template('kart.html')


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
            return render_template('kart.html')
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


@app.route('/kart')
def kart():
    """Search for products/items."""
    return render_template('kart.html')


@app.route('/products.json')
def get_products():
    products = db.session.query(Product).all()
    product_details = {}

    for product in products:
        product_details[product.product_id] = product.name

    return jsonify(product_details)


if __name__ == "__main__":
    connect_to_db(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///kart"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.run(host='0.0.0.0')
