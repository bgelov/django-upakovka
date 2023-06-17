# django-upakovka
Django application for managing a manual packing warehouse

![unittest status](https://github.com/bgelov/django-upakovka/actions/workflows/django-unittest.yml/badge.svg)


# May | New features

- Live counter for orders and incomings

![image](https://github.com/bgelov/django-upakovka/assets/5302940/1f851e9b-8444-4153-a354-d4e7d8ff7821)

- Custom Print buttom for Orders model (https://bgelov.ru/django/add-custom-button)

![image](https://github.com/bgelov/django-upakovka/assets/5302940/08c3fbaf-5a55-4be7-a034-201bc6312ef5)


# Database | PostgreSQL

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
