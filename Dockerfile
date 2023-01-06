FROM ubuntu:18.04

RUN DEBIAN_FRONTEND=noninteractive && \
	apt-get update && \
	apt-get install -y \
		gcc g++ gfortran \
		libc++-dev \
		libstdc++-6-dev zlib1g-dev \
		automake autoconf libtool \
		git subversion \
		libatlas3-base \
		nvidia-cuda-dev \
		ffmpeg \
		python3 python3-dev python3-pip \
		python python-dev python-pip \
		wget unzip sox git && \
	apt-get clean

ADD . /gentle
RUN cd /gentle/ext && \
       git submodule init && \
       git submodule update && \
       ./install_kaldi.sh && \
       make depend && make && rm -rf kaldi *.o

RUN cd /gentle && python3 setup.py develop
RUN cd /gentle && ./install_models.sh

EXPOSE 8765

VOLUME /gentle/webdata

CMD cd /gentle && python3 serve.py
