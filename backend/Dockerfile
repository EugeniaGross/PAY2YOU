FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--timeout", "120", "--log-level", "debug", "--bind", "0.0.0.0:8000", "backend.wsgi"]