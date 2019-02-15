#!/usr/bin/env sh

# copy license
mkdir -p wc_sandbox/assets/licenses/
cp ~/.wc/third_party/chemaxon.license.cxl wc_sandbox/assets/licenses/chemaxon.cxl

# build image
docker build \
    --tag karrlab/wc_sandbox:0.0.48
    --tag karrlab/wc_sandbox:latest
    .

# run container
docker run --env PORT=8888 --expose 8888 -P karrlab/wc_sandbox:latest
docker run --env PORT=8888 --expose 8888 -p 8888:8888 karrlab/wc_sandbox:latest

# check everything work by visiting http://localhost:8888/tree

# push image to heroku
heroku container:push web -a wc--sandbox

# deploy image
heroku container:release web -a wc--sandbox

# view log
heroku logs --tail -a wc--sandbox