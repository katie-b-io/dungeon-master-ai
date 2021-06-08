#!/bin/sh

python3 -m pytest --cov=dmai tests/ --cov-report=xml
curl -s https://codecov.io/bash -t $1
