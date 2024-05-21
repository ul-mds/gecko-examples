FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN apk update && \
    apk add --no-cache git && \
    git submodule init && \
    git submodule update --recursive && \
    pip install poetry==1.7.1 && \
    poetry install

ENTRYPOINT ["/usr/local/bin/poetry", "run", "gecko"]
CMD ["--help"]
