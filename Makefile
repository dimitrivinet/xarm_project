IMAGE_NAME=dimitrivinet/alfred


run_alfred:
	cd xarm_project/ &&	docker-compose up -d
	cd ..
	sleep 5
	brave-browser -new-tab 'http://localhost:8080'

down_alfred:
	cd xarm_project/ && docker-compose down

run_hand:
	alfred_venv/bin/python3 xarm_project/xarm_alfred_app/xarm_hand_control.py

run:
#	-sudo docker stop rasa && sudo docker rm rasa
#	-sudo docker stop alfred && sudo docker rm alfred
#	sudo docker run -dit -p 5005:5005 --name rasa dimitrivinet/rasa-api
#	sudo docker run -it --name alfred -p 8080:8080 --link rasa dimitrivinet/alfred:novosk
	docker-compose run --rm arm_control

down:
#	-docker stop rasa && sudo docker rm rasa
#	-docker stop alfred && sudo docker rm alfred
	docker-compose down

build:
	docker build -t $(IMAGE_NAME):dev .

push:
	docker push $(IMAGE_NAME):dev

build_prod:
	docker build -t $(IMAGE_NAME):latest .

push_prod:
	docker build -t $(IMAGE_NAME):latest .