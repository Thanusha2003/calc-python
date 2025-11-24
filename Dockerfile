FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt flask

# Copy application code
COPY src/ /app/src
COPY secure_api.py /app/secure_api.py

EXPOSE 5000

CMD ["python", "secure_api.py"]
