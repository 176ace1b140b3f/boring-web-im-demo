# Web IM


## Development

Upgrade deps (not essential):

    pip-compile --no-index --upgrade --output-file requirements.txt requirements.in

Testing:

    python setup.py test

Install deps:

    pip install -r requirements.txt

Create database:

    python app.py create

Start dev web app:

    python app.py runserver
    open http://127.0.0.1:5000/

Lint:

    flake8 web_im tests
