FROM karrlab/wc_env

ADD . /home
WORKDIR /home

RUN pip3.6 install -e . \
    && jupyter contrib nbextension install \
    && jupyter nbextensions_configurator enable

CMD wc-sandbox start --port $PORT --no-browser
