# django-upakovka
Django application for managing a manual packing warehouse

![unittest status](https://github.com/bgelov/django-upakovka/actions/workflows/django-unittest.yml/badge.svg)


## PostgreSQL

```
CREATE DATABASE ***;

CREATE USER django_upakovka WITH PASSWORD '************';

ALTER ROLE django_upakovka SET client_encoding TO 'utf8';
ALTER ROLE django_upakovka SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_upakovka SET timezone TO 'UTC+3';

GRANT ALL PRIVILEGES ON DATABASE *** TO ***;

# Rights for test database
CREATE DATABASE test_django_upakovka;
GRANT ALL PRIVILEGES ON DATABASE *** TO ***;

# Owner rights
ALTER DATABASE *** OWNER TO ***;

ALTER DATABASE *** OWNER TO ***;
```
