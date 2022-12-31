# package_selection
Web application to suggest user packages according to services they chosse.
## Setup Guideline
___
- create a virtual environment using `pipenv shell`
- install dependencies
- create database
- create an .env file and provide followings:
    - SECRET_KEY='YOUR_SECRET_KEY_HERE'
    - DB_NAME='YOUR_DATABASE_NAME_HERE'
    - DB_USER='YOUR_DATABASE_USERNAME_HERE'
    - DB_PASSWORD='YOUR_DATABASE_PASSWORD_HERE'
    - DB_HOST=localhost
    - DB_PORT=5432
- make migration
- load data from package_selection.sql
- create superuser
- register customer
- login and select services to get suggested packages