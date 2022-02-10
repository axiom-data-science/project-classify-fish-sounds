FROM debian:bullseye-slim

RUN apt-get update \
    && apt-get install -y pip \
    && rm -rf /var/lib/apt/lists/*

COPY acoustic-tools /tmp
RUN pip install -e /tmp
