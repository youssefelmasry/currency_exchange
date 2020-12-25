from django.http import response
from django.test import client
from rest_framework.test import APITestCase
from rest_framework import status
from rate.models import Rate

class RateCurrencyExchangeTest(APITestCase):
    def setUp(self):
        self.rate_api = "/rate/"

    def test_currency_not_provided(self):
        response = self.client.get(path=f"{self.rate_api}?to_currency=USD&date=2005-06-25")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["status"], "Please you should provide two currencies")

    def test_currency_not_found(self):
        response = self.client.get(path=f"{self.rate_api}?from_currency=EUR&to_currency=Uld&date=2002-09-22")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["status"], "Not Found")

    def test_wrong_date_format(self):
        date = "2222-66-888"
        response = self.client.get(path=f"{self.rate_api}?date={date}&to_currency=USD&from_currency=EUR")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["status"], f"time data '{date}' does not match format '%Y-%m-%d'")

    def test_date_not_provided(self):
        response = self.client.get(path=f"{self.rate_api}?to_currency=USD&from_currency=AUD")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if the result saved in database
        self.assertEqual(response.json()['data']['rate'], f'1 AUD = {Rate.objects.last().rate} USD')

