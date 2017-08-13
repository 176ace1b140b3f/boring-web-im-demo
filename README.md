# Web IM


## Development

Upgrade deps:

> pip-compile --no-index --output-file requirements.txt requirements.in

Create database:

> python app.py create

Testing:

> python setup.py test

Start dev web app:

> python app.py runserver

## Entrypoints

```
/api/user/register
/api/user/login
/api/user/logout
```
