#FROM python:3.6
#WORKDIR /
#COPY requirements.txt ./
#RUN pip install --upgrade setuptools
#RUN pip install -r requirements.txt
#COPY . .
#CMD [ "python", "./program.py" ]

FROM python:3.6
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /opt/example1/
WORKDIR /opt/example1
CMD ["python","-u","program.py"]

#COPY . /app
#WORKDIR /app
#RUN pip install -r requirements.txt
#CMD ["python", "/app/program.py"]