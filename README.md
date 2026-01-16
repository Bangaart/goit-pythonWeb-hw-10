# Quotes Web App

Django web application for storing, adding and displaying quotes and their authors

## Tech Stack

- Python 3.13
- Django
- PostgreSQL
- MongoDB
- Beautiful Soup and requests
- Docker & Docker Compose
- Poetry

## Features

- User authentication (Log in, Log out)
- CRUD operation only for authenticated users
- Tags for quotes
- Fill database with scraped data from another site in runtime
- Custom script to migrate database from MongoDB

## How to run the project

- run command "docker compose up --build" in docker from the folder where project located
- open "http://127.0.0.1:8000" in your browser.
- than there are two ways how to fill data:
- 1 -http://127.0.0.1:8000/quotes/quotes-list - on this link there will be a button "Fill database". It scraps in real
  time this site https://quotes.toscrape.com and takes all info from it. Execution takes a time ~1 minute
- 2 - the second way is to run docker command inside container - "docker container exec web python manage.py
  migration_script" or
  via docker UX you can open EXEC tub inside quotes_web container and run python manage.py migration_script. This script
  starts migration data from MongoDB to Postgres
- all this 2 ways creates a superuser (username: admin, password: admin)

## Project Structure

```text
.
├── quotes/              # Django app  
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── manage.py
└── README.md


