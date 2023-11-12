from unittest import TestCase
from app import app

app.config['TESTING'] = True

class BloglyTestCase(TestCase):
    """Integration tests for Blogly app"""

    def test_root(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            # check to see if status code is 200 - request is successfull
            self.assertEqual(resp.status_code, 200)

            #check to see if correct h2 tag is in html for page
            self.assertIn('<h1>Blogly Home</h1>', html)

    def test_user_listing(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            # check to see if status code is 200 - request is successfull
            self.assertEqual(resp.status_code, 200)

            #check to see if correct h2 tag is in html for page
            self.assertIn('<h2>User Listing</h2>', html)

