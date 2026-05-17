# OpenBerg Terminal — Server
# Build context: apps/server  (i.e. docker-compose sets context: apps/server)
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
