FROM node:20

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python3 python3-venv python3-pip curl
RUN python3 -m venv /opt/venv

# create address file, where app will be
WORKDIR /usr/src/app

# install dependencies
COPY package*.json jest.config.ts tsconfig.json requirements.txt getKNNForDB.py python pythonTest src .env ./
RUN npm install
RUN npm run build

# !! maybe needed install dependencies for python code
# !!!!!!!!!!
# copy code into container

RUN /opt/venv/bin/pip3 install -r requirements.txt

#RUN /opt/venv/bin/pip3 install mysql-connector-python
#RUN /opt/venv/bin/pip3 install jsonschema
#RUN /opt/venv/bin/pip3 install dtw
#RUN /opt/venv/bin/pip3 install dtw-python
#RUN /opt/venv/bin/pip3 install fastdtw
#RUN /opt/venv/bin/pip3 install numpy

EXPOSE 3000

# run project
CMD ["npm", "run", "start"]