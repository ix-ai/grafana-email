FROM alpine:latest
LABEL maintainer="docker@ix.ai"

WORKDIR /app

COPY src/ /app

RUN apk --no-cache add python3 zlib-dev jpeg-dev gcc musl-dev python3-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del --purge gcc musl-dev python3-dev

ENTRYPOINT ["python3", "/app/grafana-email.py"]
