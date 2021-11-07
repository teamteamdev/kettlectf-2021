FROM python:3-alpine
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev dbus-x11 ttf-freefont xvfb firefox
RUN pip install gunicorn
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk add openjdk11
COPY geckodriver /bin/geckodriver
