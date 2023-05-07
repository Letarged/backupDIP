FROM ubuntu

#COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    cewl

ENTRYPOINT [ "cewl" ]

CMD ["--help"]