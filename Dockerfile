FROM ubuntu:20.04

RUN apt update && apt install -y git wget unzip python3-pip 

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./xarm_alfred_app app/

CMD cd /app && python3 xarm_alfred.py