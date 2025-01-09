ARG BASE=python:3.12.3-alpine3.20

FROM ${BASE} AS builder

RUN apk add --no-cache bash

SHELL ["/bin/bash", "-c"]

RUN apk add --no-cache \
    curl \
    build-base \
    alpine-sdk \
    libffi-dev \
    libsodium \
    libsodium-dev    

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN . ${HOME}/.cargo/env

COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /uvx /bin/

WORKDIR /witness
COPY . /witness

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:${PATH}

RUN pip install --upgrade pip
RUN uv sync --frozen

# Runtime layer
FROM ${BASE}

RUN apk --no-cache add \
    bash \
    alpine-sdk \
    libsodium-dev

RUN mkdir -p /usr/local/var/keri/cf

WORKDIR /witness

COPY --from=builder /witness /witness

ENV PATH="/witness/venv/bin:${PATH}"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5642
ENTRYPOINT ["/entrypoint.sh"]

