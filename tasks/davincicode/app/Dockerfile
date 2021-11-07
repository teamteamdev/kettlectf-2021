FROM python:3-alpine
RUN apk add --no-cache socat
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
