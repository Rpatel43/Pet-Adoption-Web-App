FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend
ENV PYTHONPATH=/app
EXPOSE 5000
CMD ["python", "-m", "backend.main"]
