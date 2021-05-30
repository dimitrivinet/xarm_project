IMAGE_NAME=dimitrivinet/alfred


run_alfred:
	docker-compose up -d
	sleep 5
	brave-browser -new-tab 'http://localhost:8080'

down_alfred:
	docker-compose down

run_hand:
	alfred_venv/bin/python3 xarm_project/xarm_alfred_app/xarm_hand_control.py


build:
	docker build -t $(IMAGE_NAME):dev .

push:
	docker push $(IMAGE_NAME):dev

build_prod:
	docker build -t $(IMAGE_NAME):latest .

push_prod:
	docker build -t $(IMAGE_NAME):latest .