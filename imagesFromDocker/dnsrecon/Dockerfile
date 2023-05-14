FROM ubuntu

RUN apt update && apt install -y \
    dnsrecon

ENTRYPOINT [ "dnsrecon" ]

CMD ["--help"]