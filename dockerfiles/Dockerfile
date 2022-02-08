FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./requirements.txt /app

RUN apt-get update && apt-get install libpq-dev gcc  -y
RUN pip install pip --upgrade
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

CMD ["gunicorn", "-w", "2", "--bind", ":8000", "biblioteca.app:create_app()", "--worker-class", "uvicorn.workers.UvicornWorker"]