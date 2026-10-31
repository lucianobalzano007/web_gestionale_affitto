FROM python:3.12.16-alpine

WORKDIR /app
# Crea un utente non privilegiato
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

# Installa prima le dipendenze per sfruttare la cache Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

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

RUN chown -R appuser:appgroup /app

USER appuser

CMD [ "python","application.py"]