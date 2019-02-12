FROM karrlab/wc_env_dependencies

RUN git clone https://github.com/KarrLab/wc_sandbox.git \
    && pip3.6 install -e wc_sandbox \
    && jupyter contrib nbextension install \
    && jupyter nbextensions_configurator enable \
    && wc-sandbox install-packages \
    && wc-sandbox get-notebooks \
    && pgcontents init -l $DATABASE_URL --no-prompt

CMD wc-sandbox start --port $PORT --no-browser
