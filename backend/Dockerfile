
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./backend/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4"]
