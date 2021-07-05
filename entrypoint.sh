#!/bin/bash

if [ -z ${BUILD_ENV} ]; then
    # Deploy build - run tests
    cd /app/dungeon-master-ai
    python3 -m pytest --cov=dmai tests/ --cov-report=xml
    bash <(curl -s https://codecov.io/bash) -t $1

elif [ ${BUILD_ENV} = "DEV" ]; then
    # Dev build - run the Rasa NLU server
    python3 -m rasa run --enable-api --quiet --model /app/dungeon-master-ai/models/dmai_nlu.tar.gz

else
    # Other build
    echo "Other build"

fi
