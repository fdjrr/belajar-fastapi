# Testing Project

## Installation

```
$ python3 -m pip install virtualenv
$ virtualenv venv

# Linux
$ source venv/bin/activate

# Windows
$ venv/Scripts/activate

$ pip install -r requirements.txt

$ alembic init alembic
# set sqlalchemy.url on alembic.ini

# make migration
$ alembic revision -m '{migration name}'

# run migration
$ alembic upgrade head
```