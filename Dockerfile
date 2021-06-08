# ----------------------------------- Base ----------------------------------- #
FROM ubuntu:20.04 AS base

WORKDIR /app
COPY . /app

RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get install -y --no-install-recommends \
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

# ------------------------------- Fast-Forward ------------------------------- #
FROM base AS ff

# dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  flex \
  bison \
  && apt-get autoremove -y \
  && apt-get clean -y

# download the FF source tar and install
RUN curl https://fai.cs.uni-saarland.de/hoffmann/ff/Metric-FF-v2.1.tgz --output Metric-FF-v2.1.tgz
RUN tar -zxf Metric-FF-v2.1.tgz
RUN cd Metric-FF-v2.1 && make

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
COPY --from=ff /app/Metric-FF-v2.1 /app/planners/Metric-FF-v2.1
COPY --from=fd /app/downward /app/planners/downward

# update paths
ENV PATH="${PATH}:/usr/local/bin:/app:/app/planners/Metric-FF-v2.1:/app/planners/downward"
ENV PYTHONPATH="${PYTHONPATH}:/app"

# install dungeon master requirements
RUN cd /app && \
  poetry config virtualenvs.create false && \
  poetry install && \
  rm -rf dist *.egg-info

# add entrypoint
ENTRYPOINT ["./entrypoint.sh"]
