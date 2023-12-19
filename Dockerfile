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
# RUN pip3 install git+https://github.com/ageitgey/face_recognition_models.git

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]