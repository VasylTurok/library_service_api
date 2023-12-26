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

## Img
![image](https://github.com/VasylTurok/library_service_api/assets/127683195/b54e1aab-c740-418f-8ef0-b1d60ce630c6)
![image](https://github.com/VasylTurok/library_service_api/assets/127683195/4500aab3-0576-4b60-bd04-edd1350a40aa)
![image](https://github.com/VasylTurok/library_service_api/assets/127683195/9d0da99a-09f6-4940-a113-2d5d50589806)
![image](https://github.com/VasylTurok/library_service_api/assets/127683195/e8d5e5fc-f14b-4776-a089-3e15ff3b7476)
![image](https://github.com/VasylTurok/library_service_api/assets/127683195/8b842b26-1123-4827-947b-54319c3c996b)
![image](https://github.com/VasylTurok/library_service_api/assets/127683195/5f53c8fb-c927-4ec9-ac64-3485034eb201)
