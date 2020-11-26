FROM python:3.8.5

RUN apt-get update
RUN apt-get install -y libx11-dev libglib2.0-0 libxext6 libsm6 libxrender1 gtk3.0
RUN export DISPLAY=host.docker.internal:0.0

RUN pip install --upgrade pip

WORKDIR /home/workspace

COPY requirements.txt ${pwd}

RUN pip install -r requirements.txt

RUN pip install -r mayavi PyQt5