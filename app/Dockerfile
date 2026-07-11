FROM python:3.14.6-slim

ENV PYTHONUNBUFFERED=1
ENV APP_HOST=0.0.0.0

RUN useradd --system --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app

COPY --chown=app:app app.py /app/app.py

USER app

EXPOSE 8000

CMD ["python3", "app.py"]