#!/bin/bash

python3 -m pytest --cov=dmai tests/ --cov-report=xml
bash <(curl -s https://codecov.io/bash) -t $1