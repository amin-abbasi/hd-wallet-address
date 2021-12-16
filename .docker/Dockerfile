# syntax=docker/dockerfile:1
FROM python:3.9.5
RUN su root

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update
RUN python3 -m venv venv

COPY requirements.txt requirements.txt

RUN . venv/bin/activate
RUN pip3 install -r requirements.txt
RUN pip3 install py_crypto_hd_wallet
RUN pip install --upgrade pip

EXPOSE 5000

COPY . .
CMD ["flask", "run"]
