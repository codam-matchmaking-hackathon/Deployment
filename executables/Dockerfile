FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    g++ \
    make \
    && rm-rf /var/lib/apt/lists/*

COPY ./tools/ /tmp/

RUN pip3 install -r /tmp/dependencies.txt
WORKDIR /app

COPY ./source/ ./

CMD ["python3", "/tmp/app.py"]
