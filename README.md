# ***RESOURCES***

## ***(Create a platform for manage resources like cars or houses and their reservations)***  

## PROJECT PRESENTATION

This project is a web plateform that will allow anyone to find and reserve a resource (cars, apartment, ...).
It also have prety advanced admin interface to allow admin to manage with ease all entities aroundin this app.

## DOWNLOAD AND RUN THE PROJECT

1.  Clone the project
    
    git clone https://github.com/vector22/resources

2.  Create a virtual environment and activate it

    cd resources && virtualenv -p python3.8 env  
    source env/bin/activate

3. Install requirements file

    pip install -r requirements.txt

4. Migrate the database
    
    ./manage.py migrate

5.  Create a super user

    ./manage.py createsuperuser

6.  Run the development server

    ./manage.py runserver

7. (optional) Run Memcached to use caching content on the app
    memcached -l 127.0.0.1:11211 | Download and install memcached https://memcached.org/downloads.

8. (optional) Run some tests
    ./manage.py test


Now you need to populate the database by add some resources and reservations through the admin panel.
    
## API USAGE AND FEATURES

An API  has been added to the project as required by the second party of the test.
But some enlightenment must be done to be able to play with it.

First thing to note is that the **Authentication method used is [JWT](https://jwt.io/)**,
because it is more modern and offer more flexibility when using it.
So, to have access to the API you need to be authenticated for all requests.

###  1. Get the token
Use the *httpie* here for demo. But you can use *curl*,*postman* or what you want.

    `http post http://127.0.0.1:8000/api/v1/token/ username=matas password=M4TM4Pass`

expected result if the credentials are corrects : 
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQ1MjI0MjU5LCJqdGkiOiIyYmQ1NjI3MmIzYjI0YjNmOGI1MjJlNThjMzdjMTdlMSIsInVzZXJfaWQiOjF9.D92tTuVi_YcNkJtiLGHtcn6tBcxLCBxz9FKD3qzhUg8",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0NTMxMDM1OSwianRpIjoiMjk2ZDc1ZDA3Nzc2NDE0ZjkxYjhiOTY4MzI4NGRmOTUiLCJ1c2VyX2lkIjoxfQ.rA-mnGRg71NEW_ga0sJoaMODS5ABjE5HnxJDb0F8xAo"
}
```

### 2. Access the protected views on the backend

```
http http://127.0.0.1:8000/api/v1/ "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQ1MjI0MjAwLCJqdGkiOiJlMGQxZDY2MjE5ODc0ZTY3OWY0NjM0ZWU2NTQ2YTIwMCIsInVzZXJfaWQiOjF9.9eHat3CvRQYnb5EdcgYFzUyMobXzxlAVh_IAgqyvzCE"
```

expected output (be sure to have some resources objects created in the admin first) :
```

    {
        "address_line": "Cocody deux plateaux bvd latrille",
        "city": "Abidjan",
        "country": "Cote d'Ivoire",
        "description": "Un super studio situe a cococy bvd latrille.",
        "id": 1,
        "is_available": true,
        "name": "Mon super studio 1",
        "picture": "http://127.0.0.1:8000/media/images/resource/sutudio1.jpeg",
        "price": 6,
        "state": "civ",
        "type": 1
    },
    {
        "address_line": "Cocody riviera pqlmerais",
        "city": "Abidjan",
        "country": "Cote d'Ivoire",
        "description": "Un super studio situe a la riviera palmerais",
        "id": 2,
        "is_available": true,
        "name": "Mon super studio 2",
        "picture": "http://127.0.0.1:8000/media/images/resource/studio2.jpg",
        "price": 10,
        "state": "civ",
        "type": 1
    }
]
```
By default the **access token is configured for 15 mins as lifetime** but you can change it in the project `settings`
file, by udating the `ACCESS_TOKEN_LIFETIME` value of `SIMPLE_JWT` dict.

### 3. To get a new access token, you should use the refresh token endpoint `/api/v1/token/refresh/` posting the refresh token:

```
http post http://127.0.0.1:8000/api/v1/token/refresh/ refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0NTMwODIyMiwianRpIjoiNzAyOGFlNjc0ZTdjNDZlMDlmMzUwYjg3MjU1NGUxODQiLCJ1c2VyX2lkIjoxfQ.Md8AO3dDrQBvWYWeZsd_A1J39z6b6HEwWIUZ7ilOiPE
```
The return is a new access token that you should use in the subsequent requests.


### 4. API documentation

A documentation has been added to the API to let developers have some fun and indea of how to interact with it
from a frontend client like ReactJs or VanillaJs.
Two GUI of the same API has been provided, `api/v1/doc/` and `api/v1/redoc/`. Feel free to choose the one you love.


## Errors, bugs and improvements
This project is under development, so many features are not yet implemented.
Also try to notice me all the bugs, errors and improvements ideas you have about this app,
by sending me a email to **rekinvector@gmail.com**