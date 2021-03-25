FROM ubuntu:20.04

RUN apt update && apt install -y wget unzip python3-pip 

COPY ./xarm_alfred_app/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./xarm_alfred_app app/

# CMD bash

CMD python3 app/xarm_alfred_for_docker.py -n