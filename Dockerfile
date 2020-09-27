FROM alpine:latest
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/etherscan-exporter"

WORKDIR /grafana-email

COPY grafana-email/ /grafana-email

RUN apk --no-cache add python3 py3-pillow py3-requests && \
    pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "/grafana-email/grafana-email.py"]
