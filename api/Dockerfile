FROM python:3.7.2-alpine3.9

COPY src /src/
# install system packages required by psycopg2 (postgres adapter for python)
RUN apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /src/payments/
EXPOSE 8000
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
