# library_service_api

## Description:
The system will optimize the work of library administrators and will make the library service much more user-friendly.

## Requirements:

### User Registration and Authentication:
- Users can register with their email and password to create an account.
- Users can login with their credentials and receive a token for authentication.

### CRUD functionality for Books Service
- POST:               books/             - add new 
- GET:                 books/              - get a list of books
- GET:                 books/<id>/      - get book's detail info 
- PUT/PATCH:    books/<id>/      - update book (also manage inventory)
- DELETE:          books/<id>/      - delete book

### Borrowing functionality
- POST:            borrowings/   		                        - add new borrowing (when borrow book - inventory should be made -= 1) 
- GET:              borrowings/?user_id=...&is_active=...  - get borrowings by user id and whether is borrowing still active or not.
- GET:              borrowings/<id>/  			- get specific borrowing 
- POST: 	          borrowings/<id>/return/ 		- set actual return date (inventory should be made += 1)


### Notifications Service
- Notifications about new borrowing created in Telegram

## Installation:
- Create local copy: `git clone https://github.com/VasylTurok/library_service_api.git`
- Move to `cd library_service_api`
- Create venv: `python3 -m venv venv`
- Activate venv: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Copy .env.sample > .env and populate with required data
- `python manage.py migrate`
- Run redis server: `docker run -d -p 6379:6379 redis`
- Run Celery `celery -A library_service worker -l INFO -P solo`
- Run app `python manage.py runserver`

## Test
Use `python manage.py test` to run tests.
