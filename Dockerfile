FROM ubuntu:latest
LABEL authors="sveto"

ENTRYPOINT ["top", "-b"]