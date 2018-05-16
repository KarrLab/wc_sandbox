FROM karrlab/build:0.0.23

RUN rm ~/.gitconfig

ADD . /home
WORKDIR /home

RUN pip3 install -U -r requirements.txt

CMD ./start_jupyter
