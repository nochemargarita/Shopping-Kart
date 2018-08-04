from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, session, request
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Return homepage."""

    return render_template('homepage.html')



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.run(host='0.0.0.0')
