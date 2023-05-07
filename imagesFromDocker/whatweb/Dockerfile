FROM ubuntu

#COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    whatweb

ENTRYPOINT [ "whatweb" ]

CMD ["--help"]