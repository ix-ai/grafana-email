FROM alpine:latest
LABEL maintainer="docker@ix.ai"

WORKDIR /app

COPY src/ /app

RUN apk --no-cache add python3 py3-pillow py3-requests && \
    pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "/app/grafana-email.py"]
