import unittest
from server import app
from model import connect_to_db, db, example_data, Customer
from flask import session, url_for


class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Already a customer?", result.data)
        self.assertIn(b"Sign Up", result.data)
        self.assertIn('Log In', result.data)

        self.assertNotIn('Welcome', result.data)
        self.assertNotIn('Log Out', result.data)

    def test_signup(self):
        """Test the sign up route."""

        result = self.client.get("/")
        self.assertIn('First Name', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)
        self.assertIn('Phone', result.data)
        self.assertIn('Already a customer?', result.data)

        self.assertNotIn('MY KART', result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.get("/")
        self.assertIn("email", result.data)
        self.assertIn("password", result.data)

    def test_logout(self):
        """Test logout functionality."""

        with self.client as c:
            with c.session_transaction() as session:
                session['email'] = 'sp@y'

        result = self.client.get("/logout", follow_redirects=True)

        with self.client as c:
            with c.session_transaction() as session:
                assert session == {}

        self.assertEqual(result.status_code, 200)
        self.assertIn("Log In", result.data)
        self.assertIn("Sign Up", result.data)

    def test_shopping(self):
        """Test the page when user is logged in."""
        with self.client as c:
            with c.session_transaction() as session:
                session['email'] = 'sp@y'

        result = self.client.get('/shop')

        self.assertIn('Log out', result.data)
        self.assertIn('Search', result.data)
        self.assertIn('Add', result.data)
        self.assertIn('MY KART', result.data)
        self.assertIn('Item', result.data)
        self.assertIn('Quantity', result.data)
        self.assertIn('Remove/Add', result.data)

        self.assertNotIn('Sign Up', result.data)
        self.assertNotIn('Log In', result.data)

    def test_kart(self):
        """Test the page when user is logged in."""
        with self.client as c:
            with c.session_transaction() as session:
                session['email'] = 'sp@y'

        result = self.client.get('/kart')

        pass


if __name__ == "__main__":
    import unittest

    unittest.main()

