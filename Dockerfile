FROM python:3.10-slim
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/boonbot

COPY ./boonbot/ ./boonbot/
COPY ./run.py .
COPY ./start.sh .
CMD ["bash", "start.sh"]
