# Test API application

## AWS system diagram

![](files/aws-architecture.png)

## Local development & deployment

Prerequisites
- Docker
- Docker Compose

To start the application, run the following command:
```shell
docker-compose up
```

Once the application is running, it will be accessible at: http://localhost:8888 

## Local testing

1. Deploy the application using Docker Compose. 
2. Set up the environment:
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-tests.txt
```
3. Run unit tests:
```shell
python tests/unit.py
```
