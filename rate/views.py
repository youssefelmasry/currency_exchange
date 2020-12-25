from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rate.models import Rate

from requests import get
from datetime import datetime

class RateView(APIView):

    # Allow only get method for this api
    http_method_names = [u'get']

    """
    It is not a good practice to make validation in Views, it should be done in serializer, 
    but this is just for this simple API task
    """

    def validate(self):
        """
        Validation method that validate if from_currency or to_currency are not provided or blank, and date format
        If date not provided or blank, set it by default latest date
        return an error message
        """

        if not (self.from_currency and self.to_currency):
            return "Please you should provide two currencies"
        if not self.date:
            self.date = "latest"
        else:
            try:
                datetime.strptime(self.date, "%Y-%m-%d")
            except ValueError as err:
                return str(err)

    def get(self, request):
        """
        get method that handles request and response for the rate of currency exchange
        """

        # get query params data
        self.from_currency = request.query_params.get('from_currency', None)
        self.to_currency = request.query_params.get('to_currency', None)
        self.date = request.query_params.get('date', None)

        # perform simple validation on query params
        is_not_valid = self.validate()
        if is_not_valid:
            return Response({"data":None, "status":is_not_valid}, status=status.HTTP_400_BAD_REQUEST)

        # try to fetch data from database if exist, else get it from external API and save it in database
        try:
            rate = Rate.objects.get(from_currency=self.from_currency, to_currency=self.to_currency, date=self.date).rate

        except:
            response = get(f"https://www.frankfurter.app/{self.date}?from={self.from_currency}&to={self.to_currency}")

            if response.status_code != 200:
                return Response({"data":None, "status":response.reason}, status=status.HTTP_404_NOT_FOUND)

            rate = response.json()["rates"][self.to_currency]
            self.date = response.json()['date']

            # Create a record with the two currencies rate
            Rate.objects.create(from_currency=self.from_currency, to_currency=self.to_currency, date=self.date, rate=rate)

        return Response({"data":{
                                "date":self.date, 
                                "rate":f"1 {self.from_currency} = {rate} {self.to_currency}"
                                }, 
                        "status":"Successful"})
