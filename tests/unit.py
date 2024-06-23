"""
Unit tests
"""
import unittest
import json
import requests

class ApiTestCase(unittest.TestCase):
    """
    Test cases for API
    """
    def setUp(self):
        """
        Set up a base URL and session
        """
        self.base_url = 'http://localhost:8888'
        self.session = requests.Session()

    def test_health_check(self):
        """
        Test health check endpoint
        """
        url = f"{self.base_url}/health"
        response = self.session.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')

    def test_add_user(self):
        """
        Test adding a correct user
        """
        url = f"{self.base_url}/hello/testuser"
        response = self.session.put(
            url,
            data=json.dumps({'dateOfBirth': '1990-01-01'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 204)

    def test_add_wrong_user(self):
        """
        Test adding a user with incorrect username (not only letters)
        """
        url = f"{self.base_url}/hello/testuser2"
        response = self.session.put(
            url,
            data=json.dumps({'dateOfBirth': '1990-01-01'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

    def test_add_wrong_birthday(self):
        """
        Test adding a user with wrong birthday
        """
        url = f"{self.base_url}/hello/testuser2"
        response = self.session.put(
            url,
            data=json.dumps({'dateOfBirth': '2025-01-01'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        """
        Test getting an existing user
        """
        url = f"{self.base_url}/hello/testuser"

        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, testuser!', response.json()['message'])

    def test_user_not_found(self):
        """
        Test getting a non-existing user
        """
        url = f"{self.base_url}/hello/nonexistentuser"

        response = self.session.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'User not found')

    def tearDown(self):
        """
        Close the session
        """
        self.session.close()

if __name__ == '__main__':
    unittest.main()
