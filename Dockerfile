FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn pudding_server:app --bind 0.0.0.0:5000
