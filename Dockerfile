FROM arm64v8/ubuntu:20.04

RUN apt update && apt install -y wget unzip python3-pip 

COPY ./xarm_alfred_app/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./xarm_alfred_app app/

RUN rm -rf app/voice_recog_vosk/model

# CMD bash

CMD wget -O model.zip https://alphacephei.com/vosk/models/vosk-model-fr-0.6-linto-2.2.0.zip && \ 
   unzip model.zip && mv vosk-model-fr-0.6-linto-2.2.0/ app/voice_recog_vosk/model && \
    python3 app/xarm_alfred_for_docker.py -n