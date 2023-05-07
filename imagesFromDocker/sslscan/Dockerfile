FROM ubuntu

#COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    sslscan

ENTRYPOINT [ "sslscan" ]

CMD ["--help"]