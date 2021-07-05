# ----------------------------------- Base ----------------------------------- #
FROM ubuntu:20.04 AS base

WORKDIR /app
COPY . /app/dungeon-master-ai

RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get install -y --no-install-recommends \
  wget \
  curl \
  python3.8 \
  python3-venv \
  python3-pip \
  git \
  git-lfs \
  nano \
  apt-transport-https \
  ca-certificates \
  && apt-get autoremove -y \
  && apt-get clean -y
RUN update-ca-certificates

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.8 -
ENV PATH="${PATH}:/root/.poetry/bin"

# install rasa
RUN pip install rasa

# ------------------------------- FastDownward ------------------------------- #
FROM base AS fd

# dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  cmake \
  g++ \
  make \
  && apt-get autoremove -y \
  && apt-get clean -y

# download the FD git repo and install
RUN git clone https://github.com/aibasel/downward.git
RUN cd downward && \
  ./build.py

# -------------------------------- Final stage ------------------------------- #
FROM base as final

# copy directories
COPY --from=fd /app/downward /app/planners/downward

# update paths
ENV PATH="${PATH}:/usr/local/bin:/app/dungeon-master-ai:/app/planners/downward"
ENV PYTHONPATH="${PYTHONPATH}:/app/dungeon-master-ai"

# install dungeon master requirements
RUN cd /app/dungeon-master-ai && \
  poetry config virtualenvs.create false && \
  poetry install && \
  rm -rf dist *.egg-info

# train the Rasa NLU model
RUN cd /app/dungeon-master-ai && \
  python3 -m rasa train nlu --fixed-model-name dmai_nlu

# add entrypoint
ARG BUILD_ENV
ENV BUILD_ENV=${BUILD_ENV}
ENTRYPOINT ["/app/dungeon-master-ai/entrypoint.sh"]
