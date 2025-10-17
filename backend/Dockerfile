FROM python:3.10.14-slim

WORKDIR /backend

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3020

#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "3020"]

# Используем 3 воркера для параллельной обработки запросов
CMD ["gunicorn", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "1200", "--bind", "0.0.0.0:3020", "--preload", "api:app"]