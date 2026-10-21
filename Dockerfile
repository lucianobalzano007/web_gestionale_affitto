FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY static /app/static
COPY contratto.py /app
COPY file_manager.py /app
COPY finicial.py /app
COPY ric_create.py /app
COPY ricevuta.py /app
COPY user.py /app
COPY data_manager.py /app
COPY crypto.py /app
COPY application.py /app
COPY templates /app/templates
COPY db_manager.py /app

CMD [ "python","application.py"]