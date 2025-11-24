FROM python:3.10-slim

WORKDIR /app

COPY src/ /app/src
COPY secure_api.py /app/secure_api.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
RUN pip install flask

EXPOSE 5000

CMD ["python", "secure_api.py"]
