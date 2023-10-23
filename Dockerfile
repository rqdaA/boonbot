FROM ubuntu:22.04
RUN apt update && apt upgrade -y && apt install -y git python3.10 python-is-python3 python3-pip
WORKDIR /opt/boonbot
COPY ./boonbot/ /opt/boonbot/boonbot/
COPY ./requirements.txt .
COPY ./run.py .
COPY ./start.sh .
RUN pip install -r requirements.txt
CMD bash start.sh
