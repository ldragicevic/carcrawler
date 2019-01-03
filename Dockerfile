#FROM python:3.6
#WORKDIR /
#COPY requirements.txt ./
#RUN pip install --upgrade setuptools
#RUN pip install -r requirements.txt
#COPY . .
#CMD [ "python", "./program.py" ]

FROM python:3.6

RUN sudo apt-get install -y chromium-browser

RUN apt-get install -y libglib2.0-0=2.50.3-2 \
    libnss3=2:3.26.2-1.1+deb9u1 \
    libgconf-2-4=3.2.6-4+b1 \
    libfontconfig1=2.11.0-6.7+b1


ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /opt/example1/
WORKDIR /opt/example1
CMD ["python","-u","program.py"]

#COPY . /app
#WORKDIR /app
#RUN pip install -r requirements.txt
#CMD ["python", "/app/program.py"]