FROM ubuntu:bionic
RUN apt-get update && apt-get install -y make python3 python3-pip vim python3-venv git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-tk
