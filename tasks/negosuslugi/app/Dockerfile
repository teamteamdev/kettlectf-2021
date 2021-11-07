FROM python:3-alpine
RUN apk add --no-cache gcc g++ make libffi-dev openssl-dev py3-pycryptodome musl-dev linux-headers
RUN pip install gunicorn
RUN apk add --no-cache freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
