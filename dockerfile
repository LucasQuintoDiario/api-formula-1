FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn my_app:app --host 0.0.0.0 --port 8000 & streamlit run app_streamlit.py --server.port 8501"]