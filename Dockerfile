FROM python:3.9-alpine
WORKDIR /app
COPY src/monitor.py .
CMD ["python", "monitor.py"]
