# built-in packages
import unittest

# internal packages
from src.config import test_env
from src.api import create_app
from src.dal.database import initialize_database


class TestAuthApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        initialize_database(env=test_env)
        cls.env = test_env
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["WTF_CSRF_ENABLED"] = False 
        cls.client = cls.app.test_client()
        
    def setUp(self):
        with self.client.session_transaction() as sess:
            sess.clear()

    # ---Tests for login route---

    def test_login_get_positive(self):
        """
        positive test: get login page.
        """
        res = self.client.get(f"/{self.env}/login")
        self.assertEqual(res.status_code, 200)
        self.assertIn("התחברות", res.data.decode())


    def test_login_post_positive(self):
        """
        positive test: user login.
        """
        res = self.client.post(f"/{self.env}/login", data={
            "email": "admin@gmail.com",
            "password": "1234"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("חופשות", res.data.decode())


    def test_login_post_negative_missing_fields(self):
        """
        Negative test: missing_fields.
        """
        res = self.client.post(f"/{self.env}/login", data={
            "email": "", "password": ""
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("נא למלא את כל השדות", res.data.decode())


    def test_login_post_negative_wrong_credentials(self):
        """
        Negative test: wrong_credentials.
        """
        res = self.client.post(f"/{self.env}/login", data={
            "email": "nonexistent@gmail.com",
            "password": "wrongpass"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("אימייל או סיסמה שגויים", res.data.decode())


    # ---Tests for register route---

    def test_register_get_positive(self):
        """
        positive test: get register page.
        """
        res = self.client.get(f"/{self.env}/register")
        self.assertEqual(res.status_code, 200)
        self.assertIn("הרשמה", res.data.decode())


    def test_register_post_positive(self):
        """
        positive test: user register.
        """
        res = self.client.post(f"/{self.env}/register", data={
            "firstName": "Test",
            "lastName": "User",
            "email": "unique_test@example.com",
            "password": "1234"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("חופשות", res.data.decode())


    def test_register_post_negative_missing_fields(self):
        """
        Negative test: missing_fields.
        """
        res = self.client.post(f"/{self.env}/register", data={
            "firstName": "", "lastName": "", "email": "", "password": ""
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("נא למלא את כל השדות", res.data.decode())


    def test_register_post_negative_invalid_email(self):
        """
        Negative test: invalid_email.
        """
        res = self.client.post(f"/{self.env}/register", data={
            "firstName": "Test",
            "lastName": "User",
            "email": "notanemail",
            "password": "1234"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("נא להזין כתובת אימייל חוקית", res.data.decode())


    def test_register_post_negative_existing_email(self):
        """
        Negative test: existing_email.
        """
        res = self.client.post(f"/{self.env}/register", data={
            "firstName": "Test",
            "lastName": "User",
            "email": "admin@gmail.com",
            "password": "1234"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("אימייל זה כבר קיים במערכת", res.data.decode())


    # ---Tests for logout route---

    def test_logout_positive(self):
        """
        positive test: user logout.
        """
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["role_id"] = 2
            sess["user_name"] = "shir"

        res = self.client.get(f"/{self.env}/logout", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("התחברות", res.data.decode())

#
