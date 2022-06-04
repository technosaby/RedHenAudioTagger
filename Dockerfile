FROM debian:stable-slim

RUN \
  sed -i 's/stable\/updates/stable-security/g' /etc/apt/sources.list && \
  apt-get update && \

RUN apt-get install python3 \
    pip3 \
    ffmpeg

RUN pip3 install numpy \
    scikit-learn \
    pytorch \
    nltk \
    matplotlib \
    h5py \
    opencv-python

ADD . /mypackage/

ENTRYPOINT ["python", "-m", "mypackage.script"]
