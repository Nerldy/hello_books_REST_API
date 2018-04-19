[![Build Status](https://travis-ci.org/Nerldy/hello_books_REST_API.svg?branch=master)](https://travis-ci.org/Nerldy/hello_books_REST_API)
[![Coverage Status](https://coveralls.io/repos/github/Nerldy/hello_books_REST_API/badge.svg?branch=master)](https://coveralls.io/github/Nerldy/hello_books_REST_API?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/87e75c4187bfa5f7212f/maintainability)](https://codeclimate.com/github/Nerldy/hello_books_REST_API/maintainability)

# HELLO BOOKS APP
Hello-Books is a simple application that helps manage a library and its processes like stocking, tracking and renting books. With this application users are able to find and rent books. The application also has an admin section where the admin can do things like add books, delete books, increase the quantity of a book etc

## Endpoints

| Endpoints                          	| Description                 	|
|------------------------------------	|-----------------------------	|
| POST /api/v1/books                 	| add book                    	|
| PUT /api/v1/books/{book_id}        	| modify a book's information 	|
| DELETE /api/v1/books/{book_id}     	| delete a book               	|
| GET /api/v1/books                  	| retrieves all books         	|
| GET /api/v1/{book_id}              	| get a book                  	|
| POST /api/v1/users/books/{book_id} 	| borrow a book               	|
| POST /api/v1/auth/register         	| create user account         	|
| POST /api/v1/auth/login            	| logs in user                	|
| POST /api/v1/auth/logout           	| logs out user               	|
| POST /api/v1/auth/reset-password   	| reset user password         	|

## API Documentation

https://app.apiary.io/hellobooks14
