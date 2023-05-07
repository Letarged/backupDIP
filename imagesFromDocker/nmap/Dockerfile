FROM ubuntu

COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    nmap 

ENTRYPOINT [ "nmap" ]

CMD ["--help"]