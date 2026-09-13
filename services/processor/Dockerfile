FROM python:3.14-slim

WORKDIR /app

COPY services/processor/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY services/processor ./services/processor

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "services/processor/app.py"]
