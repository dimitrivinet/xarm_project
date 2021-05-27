FROM ubuntu:20.04

RUN apt update && apt install -y git wget unzip python3-pip 

COPY ./xarm_alfred_app/requirements.txt requirements.txt
# add model dir to dockerignore

RUN pip3 install -r requirements.txt

RUN pip3 install git+https://github.com/xArm-Developer/xArm-Python-SDK.git

COPY ./xarm_alfred_app app/

CMD bash