import unittest
import sqlite3
import os

from app import app


class FakeNewsAppTest(unittest.TestCase):

    def setUp(self):

        app.config["TESTING"] = True

        self.client = app.test_client()

    def test_home_page(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_about_page(self):

        response = self.client.get("/about")

        self.assertEqual(response.status_code, 200)

    def test_login_page(self):

        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)

    def test_register_page(self):

        response = self.client.get("/register")

        self.assertEqual(response.status_code, 200)

    def test_admin_login_page(self):

        response = self.client.get("/admin/login")

        self.assertEqual(response.status_code, 200)

    def test_api_health(self):

        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)

    def test_invalid_prediction(self):

        response = self.client.post(
            "/api/predict",
            json={}
        )

        self.assertNotEqual(response.status_code, 200)

    def test_database_exists(self):

        self.assertTrue(
            os.path.exists("database/database.db")
        )

    def test_database_connection(self):

        conn = sqlite3.connect(
            "database/database.db"
        )

        self.assertIsNotNone(conn)

        conn.close()


if __name__ == "__main__":

    unittest.main()
