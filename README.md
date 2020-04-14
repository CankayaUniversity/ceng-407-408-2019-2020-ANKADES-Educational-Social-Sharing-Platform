# ANKADES EDUCATIONAL SOCIAL SHARING PLATFORM

Welcome to Ankades Social Educational Sharing Platform

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

**Download Postgresql : https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1257371**

You dont need to install stackbuilder.

**Create a database then change your database login information in ankadescankaya->settings.py in _DATABASES_**

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yourdbname', #database name
        'USER': 'yourusername', #username
        'PASSWORD': 'yourpassword', #database password
        'HOST': '127.0.0.1', #localhost
        'PORT': 'postgresqlport'# can be 5432 or 5433 or something else
        }
    }
```

**CREATE SUPER USER:** Activate the virtual environment on your terminal.

```
python manage.py createsuperuser
```

**ADDING HOME CATEGORY

120523ef-de49-4f5a-9ada-63362d72070a  -> Copy this UUID and paste it to ArticleCategory "table" -> id and parentId.

You have to fill creator_id field with your superuser's UUID which is in Account "table".

On Windows:

```
cd wvenv/Scripts
activate.bat
```

On Linux/MacOS:

```
cd env/bin
activate
```

### Installing

```
pip install -r requirements.txt
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py collectstatic
```

## Running the tests

```
python manage.py runserver
```

## Built With

* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com/)
* [Postgresql](https://www.postgresql.org/)
* [Javscript](https://www.javascript.com/)

## Authors

* **Buğra Ahmet Çağlar** - *Github* - [bugraahmetcaglar](https://github.com/bacaglar) - *Email* - [bugraahmetcaglar@gmail.com]()
* **Furkan Anıl Erdem** - *Github* - [fanilerdem](https://github.com/fanilerdem) - *Email* - [blackspike06@gmail.com]()
* **Nihan Nur Aydın** - *Github* - [ninanaydin](https://github.com/nihanaydin) - *Email* - [nihannuraydin@gmail.com]()

See also the list of [contributors](https://github.com/CankayaUniversity/ceng-407-408-2019-2020-ANKADES-Educational-Social-Sharing-Platform/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
