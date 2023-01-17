# Build stage: install pip dependencies
FROM ubuntu:20.04 AS builder

ARG VERSION
ARG PIP_EXTRA_INDEX_URL

WORKDIR /home/python-dev

# Install all the supported versions of python using the PPA and other useful tools
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common=0.99.9.8 && \
  add-apt-repository ppa:deadsnakes/ppa -y && apt-get update && apt-get install -y --no-install-recommends \
  curl=7.68.0-1ubuntu2.15

# Install pip for the desired python version
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
  python3.8 get-pip.py && \
  python3.8 -m pip install --upgrade pip==21.1.1

# Install dependencies and application
COPY requirements.txt .
COPY dist/virus_total_telegram_bot-${VERSION}-cp38-cp38m-*.whl /home/python-dev
RUN python3.8 -m pip --no-cache-dir install --user --upgrade --ignore-installed --extra-index-url "${PIP_EXTRA_INDEX_URL}" -r ./requirements.txt
RUN python3.8 -m pip --no-cache-dir install --user --upgrade --ignore-installed --no-index --no-deps --find-links /home/python-dev virus_total_telegram_bot==${VERSION}

# Final stage: install python and copy dependencies from build stage
FROM ubuntu:20.04

ARG BUILD_DATE
ARG VERSION
ARG REVISION

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Install Python
WORKDIR /usr/local/bin
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common=0.99.9.8 && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  tini=0.18.0-1 && \
  apt-get clean && \
  rm -Rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Get all the Python packages installed on the previous stage
COPY --from=builder /home/python-dev/.local/lib/python3.8/site-packages /usr/local/lib/python3.8/dist-packages
COPY --from=builder /home/python-dev/.local/bin/* /usr/local/bin/

# Create a non-root user to run the container. This step is optional, you can also use any existing user such as `www-data` for web servers (nginx for example)
RUN groupadd -g 1000 virus_total_telegram_bot && useradd -ms /bin/bash -u 1000 -g 1000 virus_total_telegram_bot

# Image labels (OCI spec)
LABEL org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.authors='clarriu97 <larriucarlos@gmail.com>' \
    org.opencontainers.image.url='https://github.com/clarriu97/virus-total-telegram-bot' \
    org.opencontainers.image.documentation='https://github.com/clarriu97/virus-total-telegram-bot' \
    org.opencontainers.image.source='https://github.com/clarriu97/virus-total-telegram-bot' \
    org.opencontainers.image.version="${VERSION}" \
    org.opencontainers.image.revision="${REVISION}" \
    org.opencontainers.image.title='virus_total_telegram_bot' \
    org.opencontainers.image.description='A telegram bot for quick checks on the security of files, URLs and other resources.' \
    org.opencontainers.image.licenses="COPYRIGHT"

USER virus_total_telegram_bot

ENTRYPOINT ["tini", "--"]
CMD ["virus_total_telegram_bot", "run"]
