import unittest, sys, os

sys.path.append('../flask_test') # imports python file from parent directory
from acnh_frontend import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    ###############
    #### tests ####
    ###############

    def search(self, villagerID):
        return self.app.post('/',
                            data=dict(villagerID=villagerID,
                            follow_redirects=True))

    def test_valid_search(self):
        response = self.search(50)
        self.assertEqual(response.status_code, 200)

    def test_invalid_search_range(self):
        response = self.search(999)
        self.assertIn(b'Number must be between 1 and 391.', response.data)
        response = self.search(-1)
        self.assertIn(b'Number must be between 1 and 391.', response.data)
    
    def test_invalid_search_noinput(self):
        response = self.search('')
        self.assertIn(b'This field is required.', response.data)


if __name__ == "__main__":
    unittest.main()