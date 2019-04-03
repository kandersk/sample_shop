# sample_shop


## Building docker container:
While in this directory

docker build -t flaskrunner:latest .

## To run container:
docker run -it -v `pwd`:/web -p 5000:5000 flaskrunner

python3 main.py