


run:
	-sudo docker stop rasa && sudo docker rm rasa
	-sudo docker stop alfred && sudo docker rm alfred
	sudo docker run -dit -p 5005:5005 --name rasa dimitrivinet/rasa-api
	sudo docker run -it --name alfred -p 8080:8080 --link rasa dimitrivinet/alfred:novosk

build:
	sudo docker build -t dimitrivinet/alfred:latest .

stop:
	-sudo docker stop rasa && sudo docker rm rasa
	-sudo docker stop alfred && sudo docker rm alfred