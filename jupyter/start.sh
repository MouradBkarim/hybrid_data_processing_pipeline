#!/bin/bash

jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --NotebookApp.token='test-token' \
  --NotebookApp.password='' \
  --NotebookApp.allow_origin='*' \
  --NotebookApp.allow_remote_access=True \
  --no-browser &

python /home/jovyan/notebook_server.py
