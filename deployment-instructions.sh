#!/usr/bin/env sh

# copy license
mkdir -p wc_sandbox/assets/licenses/
cp ~/.wc/third_party/chemaxon.license.cxl wc_sandbox/assets/licenses/chemaxon.cxl

# build image
docker rmi karrlab/wc_sandbox:0.0.51a
docker rmi karrlab/wc_sandbox:latest
docker rmi registry.heroku.com/wc--sandbox/web
docker build \
    --tag karrlab/wc_sandbox:0.0.51b \
    --tag karrlab/wc_sandbox:latest \
    .

# run container
docker run --env PORT=8888 --expose 8888 -P karrlab/wc_sandbox:latest
docker run --env PORT=8888 --expose 8888 -p 8888:8888 karrlab/wc_sandbox:latest

# check everything work by visiting http://localhost:8888/tree

# login to heroku
heroku container:login

# push image to heroku
heroku container:push web -a wc--sandbox

# deploy image
heroku container:release web -a wc--sandbox

# view log
heroku logs --tail -a wc--sandbox
