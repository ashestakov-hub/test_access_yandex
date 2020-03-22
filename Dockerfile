FROM ubuntu:18.04
RUN apt update
RUN mkdir /tests
ADD . /tests
RUN apt install python3-pip wget curl netcat libssl-dev iputils-ping -y
RUN apt install python3.7 -y
WORKDIR /tests
RUN python3.7 -m pip install -r requirements.txt