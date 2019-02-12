FROM karrlab/wc_env_dependencies

RUN pip3.6 install -e . \
    && jupyter contrib nbextension install \
    && jupyter nbextensions_configurator enable \
    && wc-sandbox install-packages \
    && wc-sandbox get-notebooks \
    && pgcontents init -l $DATABASE_URL --no-prompt

CMD wc-sandbox start --port $PORT --no-browser
