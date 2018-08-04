from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, session, request
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


@app.route('/sign-up', methods=['POST'] )
def sign_up_form():
    """Process sign-up using POST request."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')

    already_customer = db.session.query(Customer).filter(Customer.email == email).first()

    if already_customer:
        flash('Email already taken.')
        return redirect('/')
    else:
        flash('You can now start shopping.')
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            address=address)

        db.session.add(customer)
        db.session.commit()
        session['email'] = email

    return render_template('kart.html')

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.run(host='0.0.0.0')
