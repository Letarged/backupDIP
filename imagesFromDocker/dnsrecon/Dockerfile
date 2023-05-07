FROM ubuntu

#COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    dnsrecon

ENTRYPOINT [ "dnsrecon" ]

CMD ["--help"]