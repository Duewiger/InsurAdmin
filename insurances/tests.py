from django.test import  TestCase
from django.urls import reverse

from .models import Insurance


class insuranceTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.insurance = Insurance.objects.create(
            title="Harry Potter",
            author="JK Rowling",
            price="25.00",
        )

    def test_insurance_listing(self):
        self.assertEqual(f"{self.insurance.title}", "Harry Potter")
        self.assertEqual(f"{self.insurance.author}", "JK Rowling")
        self.assertEqual(f"{self.insurance.price}", "25.00")

    def test_insurance_list_view(self):
        response = self.client.get(reverse("insurance_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "insurances/insurance_list.html")

    def test_insurance_detail_view(self):
        response = self.client.get(self.insurance.get_absolute_url())
        no_response = self.client.get("/insurances/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "insurances/insurance_detail.html")