infoskjerm2 is a supersimple slideshow system (replacing the old infoskjerm)

## Install

    apt install python-dev libmysqlclient-dev
    pipenv install --dev --three
    pipenv shell
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver