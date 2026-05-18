from django.test import TestCase


class HealthcheckTests(TestCase):
    def test_healthcheck_endpoint_returns_ok(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response["X-Healthcheck"], "true")

    def test_root_endpoint_uses_healthcheck(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "manage-ai-backend")
        self.assertEqual(response["X-Healthcheck"], "true")
