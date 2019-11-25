import unittest

from libsaas.executors import requests_executor
from libsaas.services import hubspot


class IntegrationHubSpotTestCase(unittest.TestCase):
    def setUp(self) -> None:
        requests_executor.use(timeout=15.0)
        self.service_tester = hubspot.HubSpot("f14082f2-e410-4f0d-955d-d39b2c7cfc7f")

    def test_companies(self):
        resp = self.service_tester.company(2561669982).get()
        self.assertEqual(resp.get("companyId"), 2561669982)

    def test_companies_update(self):
        resp = self.service_tester.company(2561669982).update({"name": "test"})
        self.assertTrue(resp)

    def test_companies_contacts(self):
        resp = self.service_tester.company(2561669982).contacts()
        self.assertTrue(resp.get("contacts"))

    def test_company_domain(self):
        resp = self.service_tester.companies_domain("pipl.com").get()
        self.assertTrue(resp.get("results"))

    def test_companies_list(self):
        resp = self.service_tester.companies().get()
        self.assertTrue(resp.get("companies"))


class ContactIntegrationHubSpotTestCase(unittest.TestCase):
    def setUp(self) -> None:
        requests_executor.use(timeout=15.0)
        self.service_tester = hubspot.HubSpot("f14082f2-e410-4f0d-955d-d39b2c7cfc7f")

    def test_contact(self):
        resp = self.service_tester.contact("tom.raz+vettingbug@pipl.com").get()
        self.assertEqual(resp.get("vid"), 201)

    def test_contact_update(self):
        resp = self.service_tester.contact("tom.raz+vettingbug@pipl.com").update(
            {"properties": [{"property": "firstname", "value": "test"}]}
        )
        self.assertTrue(resp)

        resp = self.service_tester.contact("tom.raz+vettingbug@pipl.com").get()
        self.assertEqual(resp.get("vid"), 201)
