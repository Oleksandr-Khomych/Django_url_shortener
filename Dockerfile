FROM python:3.9.6

WORKDIR /app

COPY ./requirements.txt .

RUN python3 -m venv venv

RUN . venv/bin/activate && pip install -r requirements.txt

COPY . .

CMD python3 manage.py runserver 0.0.0.0:5000
