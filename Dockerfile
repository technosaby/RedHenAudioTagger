FROM debian:bitnami/git

RUN apt-get update \

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
