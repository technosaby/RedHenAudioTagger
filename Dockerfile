# Creation of base OS image
# FROM debian:bullseye-slim
FROM tensorflow/tensorflow:2.9.0-gpu

MAINTAINER Sabyasachi Ghosal, saby.ghosal@gmail.com

RUN apt-get -y update

RUN apt-get install --assume-yes --no-install-recommends --quiet \
        python3 \
        python3-pip \
        ffmpeg

RUN pip install --no-cache --upgrade pip setuptools
    
# Set working directory
WORKDIR /TaggingAudioEffects
RUN pwd

# Copying the folder into the local
ADD ./tagging_audio_effects .
RUN pwd

# Installing JQ required for parsing
WORKDIR /bin
RUN apt-get install -y wget
RUN wget "http://stedolan.github.io/jq/download/linux64/jq" && chmod 755 jq
RUN pwd 
# CMD ["/bin/jq"]


# View contents while building dockerfile
RUN ls -a

# Install local dependencies
RUN pip3 install -r tagging_audio_effects/requirements.txt

# Remove copied folder
RUN rm -f -r ./tagging_audio_effects
