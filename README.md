# steps to run the app
1. clone the project on your machine
1. install docker
1. run: __docker-compose up -d --build__
    * To show containers logs __docker-compose logs -f__
1. open the browser or postman and go for (http://localhost:8000/rate/)
    - Example: http://localhost:8000/rate/?date=2019-06-01&from_currency=USD&to_currency=AUD

## for tesing coverage
1. install virtualenv and make a one with python 3 
1. run: __pip install -r requirements.txt__
1. run: __coverage run manage.py test__
1. run: __coverage report__ (will generate a report on terminal) 
    * or __coverage html__ (that will generate a directory of coverage report that can be accessible through browser, just go to the coverage directory generated and open index.html)
