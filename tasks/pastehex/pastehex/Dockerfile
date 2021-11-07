FROM python:3-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install gunicorn
WORKDIR /pastehex
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt