# xArm_project
Repository for my yearly innovation project of 2021

## webspeechdemo

Demo for web speech recognition. Requirements: Flask and icecream (install via pip) and xArm SDK:

```bash
  git clone https://github.com/xArm-Developer/xArm-Python-SDK.git && cd xArm-Python-SDK && python3 setup.py install
  ```

## arm_jarvis_app

Web app for speech recognition, to be merged with arm control.

#### Launch on docker:


docker run -dit -p 5005:5005 --name rasa dimitrivinet/rasa-api

docker run -it --name alfred -p 8080:8080 --link rasa dimitrivinet/alfred
