FROM ubuntu

#COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    libpcap-dev && apt install -y masscan

ENTRYPOINT [ "masscan" ]

CMD ["--help"]