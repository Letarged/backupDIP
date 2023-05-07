FROM alpine


COPY ./nginx.txt .


#WORKDIR /app

RUN apt update && apt install -y \
    gobuster 

ENTRYPOINT [ "gobuster" ]

CMD ["dir"]
