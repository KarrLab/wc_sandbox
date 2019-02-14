FROM karrlab/wc_env_dependencies

RUN git clone https://github.com/KarrLab/wc_sandbox.git \
    && cd /root/wc_sandbox \
    && pip3.6 install --process-dependency-links -r requirements.txt \
    && pip3.6 install --process-dependency-links -e . \
    \
    && jupyter contrib nbextension install \
    && jupyter nbextensions_configurator disable \
    && jupyter nbextension enable varInspector/main \
    && jupyter nbextension enable toc2/main \
    && jupyter nbextension enable collapsible_headings/main \
    && jupyter nbextension enable equation-numbering/main \
    && jupyter nbextension enable codefolding/main \
    && jupyter nbextension enable scratchpad/main \
    && jupyter nbextension enable tree-filter/index \
    && jupyter nbextension enable printview/main \
    && jupyter nbextension disable contrib_nbextensions_help_item/main \
    \
    && cp -R wc_sandbox/assets/.jupyter/* ~/.jupyter \
    && cp wc_sandbox/assets/favicon.ico /usr/local/lib/python3.6/site-packages/notebook/static/base/images/favicon.ico \
    \
    && wc-sandbox install-packages \
    && wc-sandbox get-notebooks

CMD wc-sandbox start \
    --allow-root \
    --ip 0.0.0.0 \
    --port $PORT \
    --no-browser
