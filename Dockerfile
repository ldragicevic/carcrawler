FROM robcherry/docker-chromedriver
FROM ubuntu:17.04
FROM selenium/standalone-chrome
FROM python:3.6

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable

RUN apt update
RUN apt-get install -y libnss3 libgconf-2-4

ADD ./requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt
ADD . /opt/example1/

# rights?
RUN chmod +x /opt/example1/assets/chromedriver
WORKDIR /opt/example1

RUN whereis chromedriver
RUN whereis google-chrome

CMD ["python","-u","program.py"]
