FROM python:3.6-slim
COPY ./app.py /deploy/
COPY ./config.py /deploy/
COPY ./.env /deploy/
COPY ./feature_imports.py /deploy/
COPY ./models.py /deploy/
COPY ./helper_functions.py /deploy/
COPY ./txt_imports.py /deploy/
COPY ./wsgi.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./engine /deploy/engine/
COPY ./migrations /deploy/migrations/

WORKDIR /deploy/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["gunicorn"  , "-b", "0.0.0.0:80", "app:app"]
