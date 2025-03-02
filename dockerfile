FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "my_app:app", "--host", "0.0.0.0", "--port", "8000"]
