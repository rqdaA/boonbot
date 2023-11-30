FROM ubuntu:22.04
RUN apt update && apt upgrade -y && apt install -y git python3.10 python-is-python3 python3-pip
WORKDIR /opt/boonbot
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./boonbot/ /opt/boonbot/boonbot/
COPY ./run.py .
COPY ./start.sh .
CMD bash start.sh
