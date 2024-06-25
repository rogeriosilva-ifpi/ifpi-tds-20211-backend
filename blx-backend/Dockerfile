FROM bitnami/python:3.11.1
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD python -m uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload --reload-dir=src