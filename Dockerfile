FROM ubuntu:16.04

RUN apt-get -yqq update \
  && apt-get -yqq install python3-pip python3-dev \
  && apt-get -yqq install wget tar firefox xvfb \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN mkdir /downloads
WORKDIR /downloads

RUN wget -O package.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
RUN tar -zxvf package.tar.gz -C /usr/local/bin

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code

ENTRYPOINT ["bash", "setup_firefox.sh"]
CMD ["python", "bot.py"]