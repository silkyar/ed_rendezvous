FROM python:3.7.4-alpine3.10

# Create app directory
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3.7 install --upgrade pip
RUN pip3.7 install virtualenv
RUN virtualenv venv -p python3
RUN source venv/bin/activate
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 8000

CMD [ "sh"]