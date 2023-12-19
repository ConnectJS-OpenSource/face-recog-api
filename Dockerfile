FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip
RUN pip3 install cmake
RUN pip3 install -r requirements.txt
RUN pip3 install waitress

COPY . .
EXPOSE 8080
ENV AWS_ACCESS_KEY_ID=''
ENV AWS_SECRET_ACCESS_KEY=''
ENV AWS_DEFAULT_REGION=''
ENTRYPOINT waitress-serve --listen=*:8080 --threads=4 wsgi:app