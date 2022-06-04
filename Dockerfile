FROM bitnami/git

RUN apt-get update -qq -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    	build-essential cmake\
        python3-dev \
        python3-pip \
        ffmpeg \
        uuid-runtime \
        libgtk-3-dev \
        python3

RUN python3 -m pip install \
    numpy \ 
    scikit-learn \
    pandas \
    dlib \
    opencv-python \
    face_recognition \
    matplotlib \
    ffmpeg-python \
    ffmpeg \
    traceback2 \
    uuid \
    requests \
    wikipedia 
