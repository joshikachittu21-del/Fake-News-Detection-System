import unittest

from app import app


class APITest(unittest.TestCase):

    def setUp(self):

        app.config["TESTING"] = True

        self.client = app.test_client()

    def test_health(self):

        response = self.client.get(
            "/api/health"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_prediction(self):

        response = self.client.post(
            "/api/predict",
            json={
                "username": "Deepak",
                "news": "Scientists discover new planet."
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_history(self):

        response = self.client.get(
            "/api/history"
        )

        self.assertEqual(
            response.status_code,
            200
        )


if __name__ == "__main__":

    unittest.main()
