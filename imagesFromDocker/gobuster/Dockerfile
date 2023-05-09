FROM ubuntu

COPY ./common.txt .
COPY ./directory-list-2.3-medium.txt .
COPY ./directory-list-2.3-small.txt .
COPY ./nginx.txt .
COPY ./micro.txt .


#WORKDIR /app

RUN apt update && apt install -y \
    gobuster 

ENTRYPOINT [ "gobuster" ]

CMD ["--help"]
