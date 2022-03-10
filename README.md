# Django url shortener (test task)

## Setup
```sh
git clone https://github.com/Oleksandr-Khomych/Django_url_shortener.git
```

#### ▶️ Fill in the file .env by exiting example
```sh
cp .env.example .env
```
## ▶️Start Local
#### Create database or use SQLite(step missed)

#### Setup environment.
```sh
python -m venv venv

. venv/bin/activate

pip install -r requirements.txt

python3 manage.py migrate

DJANGO_SUPERUSER_PASSWORD=test python manage.py createsuperuser --username test --email test@test.ua --noinput

python3 manage.py runserver 0.0.0.0:8000
```

## ⚙️Run tests
```sh
python manage.py test
```

## ▶️Start in Docker-compose

```sh
sudo docker-compose up --build
```

## ❗️Create super user in Docker

#### Open bash in container
```sh
sudo docker exec -it web bash
```
Create super user
```sh
DJANGO_SUPERUSER_PASSWORD=test python manage.py createsuperuser --username test --email test@test.ua --noinput
```

#### Exit from container
```sh
exit
```
## ✅Open admin menu: http://127.0.0.1:8000/admin/

## 👤Test user auth:
#### Username: test
#### Password: test
