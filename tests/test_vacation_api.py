# built-in packages
import unittest

# internal packages
from src.config import test_env
from src.api import create_app
from src.dal.database import initialize_database


class TestVacationApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialize_database(env=test_env)
        cls.app = create_app()
        cls.app.testing = True
        cls.client = cls.app.test_client()
        
    def setUp(self):
        with self.client.session_transaction() as sess:
            sess.clear()

    # --- Tests for home_page route ---

    def test_home_page_positive(self):
        """
        positive test: get home page with authenticated user.
        """
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["role_id"] = 1
            sess["user_name"] = "shir"

        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("חופשות", res.data.decode())


    def test_home_page_negative(self):
        """
        negative test: get home page without login redirects to login.
        """
        res = self.client.get("/", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("התחברות", res.data.decode())


    # --- Tests for add_vacation route ---

    def test_add_vacation_get_positive(self):
        """
        positive test: admin can access add-vacation GET page.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2 

        res = self.client.get("/add-vacation")
        self.assertEqual(res.status_code, 200)
        self.assertIn("הוספת חופשה", res.data.decode())


    def test_add_vacation_get_negative(self):
        """
        negative test: non-admin user forbidden from add-vacation GET.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 1

        res = self.client.get("/add-vacation")
        self.assertEqual(res.status_code, 403)


    def test_add_vacation_post_positive(self):
        """
        positive test: admin submits valid form, expect success flash.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        from io import BytesIO
        dummy_image = (BytesIO(b"dummy image data"), "test.jpg")

        res = self.client.post("/add-vacation", data={
            "destination_id": "1",
            "dateRangeInput": "01/01/2030 - 05/01/2030",
            "price": "1000",
            "vacation_info": "חופשה מהממת",
            "image": dummy_image
        }, content_type="multipart/form-data", follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn("החופשה נוספה בהצלחה", res.data.decode())
    
    
    def test_add_vacation_post_negative(self):
        """
        negative test: admin submits empty form, expect error flash.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.post("/add-vacation", data={}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("יש למלא את כל השדות", res.data.decode())


    # --- Tests for edit_vacation route ---

    def test_edit_vacation_get_positive(self):
        """
        positive test: admin accesses edit-vacation GET page with valid id.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.get("/edit-vacation/4")
        self.assertEqual(res.status_code, 200)
        self.assertIn("עריכת חופשה", res.data.decode())


    def test_edit_vacation_get_negative(self):
        """
        negative test: admin requests edit page for non-existing vacation id.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.get("/edit-vacation/99999")
        self.assertEqual(res.status_code, 404)


    def test_edit_vacation_post_positive(self):
        """
        positive test: admin submits valid form on edit-vacation POST.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.post("/edit-vacation/5", data={
            "destination": "פורטוגל",
            "destination_id": "13",
            "dateRangeInput": "20/07/2025 - 30/07/2025",
            "price": "500",
            "vacation_info": "חופשה מעודכנת"
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn("החופשה עודכנה בהצלחה", res.data.decode())


    def test_edit_vacation_post_negative(self):
        """
        negative test: admin submits empty form on edit-vacation POST.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.post("/edit-vacation/3", data={}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("יש למלא את כל השדות", res.data.decode())


    # --- Tests for delete_vacation route ---

    def test_delete_vacation_positive(self):
        """
        positive test: admin deletes an existing vacation.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.post("/delete-vacation/1")
        self.assertEqual(res.status_code, 200)
        self.assertIn('"success":true', res.data.decode())


    def test_delete_vacation_negative(self):
        """
        negative test: admin tries to delete non-existing vacation.
        """
        with self.client.session_transaction() as sess:
            sess["role_id"] = 2

        res = self.client.post("/delete-vacation/99999")
        self.assertEqual(res.status_code, 404)
        self.assertIn('"success":false', res.data.decode())


    # --- Tests for toggle_like route ---

    def test_toggle_like_add_and_remove(self):
        """
        positive test: logged in user toggles like (add and then remove).
        """
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1

        # add like
        res_add = self.client.post("/like", json={"vacation_id": 7})
        self.assertEqual(res_add.status_code, 200)
        self.assertIn("Like added successfully", res_add.json["message"])

        # remove like
        res_remove = self.client.post("/like", json={"vacation_id": 7})
        self.assertEqual(res_remove.status_code, 200)
        self.assertIn("Like removed successfully", res_remove.json["message"])


    def test_toggle_like_negative_not_logged_in(self):
        """
        negative test: no user logged in (no session).
        """
        res = self.client.post("/like", json={"vacation_id": 7})
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers["Location"])
        
    
    def test_toggle_like_negative_missing_data(self):
        """
        negative test: logged in but missing vacation_id.
        """
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1

        res = self.client.post("/like", json={})
        self.assertEqual(res.status_code, 400)
        self.assertIn("Missing data", res.json["error"])

#
