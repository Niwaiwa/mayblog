# mayblog

project develop record

## structure

0. project create, packages
1. app
2. dotenv
3. custom logging
4. settings
5. error handler, return code
6. custom reponse
7. before request
8. auth method(ex. jwt...)
9. db connection
10. db schema
11. route
12. pytest, fixtures
13. api, api verification
14. dockerfile, docker-compose

## Optional

1. secrets
2. singleton
3. tox (pytest)

## alembic

```
alembic init alembic

alembic -c alembic.ini --raiseerr revision --autogenerate -m "create articles table"
PYTHONPATH=./ alembic.exe upgrade head
PYTHONPATH=./ alembic.exe upgrade +2
PYTHONPATH=./ alembic.exe downgrade base
PYTHONPATH=./ alembic.exe downgrade -1
```

## pytest

```
PYTHONPATH=./ pytest
PYTHONPATH=./ pytest --fixtures
PYTHONPATH=./ pytest --cache-clear
PYTHONPATH=./ pytest tests/test_user_article.py
```
