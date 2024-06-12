FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY . /app
COPY secrets/your-service-account-file.json /app/secrets/your-service-account-file.json

RUN pip install -r /app/requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=credentials\capstone-426202-c0124df1745c.json

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
