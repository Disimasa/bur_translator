FROM python:3.10.14-slim

WORKDIR /backend

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3020

#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "3020"]

CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "60000", "--bind", "0.0.0.0:3020", "api:app"]