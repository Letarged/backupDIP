FROM ubuntu

#COPY ./app /app

#WORKDIR /app

RUN apt update && apt install -y \
    pip \
    && pip install shcheck

ENTRYPOINT [ "shcheck.py" ]

CMD ["--help"]