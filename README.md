## Technical task Arrival

### Description

Solution for the second part of the task from Arrival.

If you'd like to run the tests locally, it's better to do it on Ubuntu 18.04.


# Run tests in Docker (recommended)
### Initialisation

See [Docker installation guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

    $ sudo docker build . -t test_task
    $ rm -rf tmp/*
    $ mkdir -p tmp/ci_artifacts
### Run tests

    $ sudo docker -v $(pwd)/tmp/:/tests/tmp run -it test_task python3.7 -m pytest --junit-xml=tmp/ci_artifacts/junit.xml -m functional

# Run tests locally
### Initialisation
    $ apt update
    $ apt install python3-pip wget curl netcat libssl-dev iputils-ping -y
    $ python3.7 -m virtualenv venv
    $ . venv/bin/activate
    
### Run tests
    $ pytest -m functional

