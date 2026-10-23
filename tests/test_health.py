import json
import unittest
from urllib.request import urlopen

class ServiceHealthTests(unittest.TestCase):

    def check_health(self, url):
        with urlopen(url, timeout=5) as response:
            self.assertEqual(response.status, 200)

            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["status"], "healthy")

    def test_auth_service(self):
        self.check_health("http://localhost:5001/health")

    def test_enter_data(self):
        self.check_health("http://localhost:5002/health")

    def test_analytics_service(self):
        self.check_health("http://localhost:5003/health")

    def test_show_results(self):
        self.check_health("http://localhost:5004/health")


if __name__ == "__main__":
    unittest.main()
