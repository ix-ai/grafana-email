FROM alpine:latest@sha256:b97e2a89d0b9e4011bb88c02ddf01c544b8c781acf1f4d559e7c8f12f1047ac3
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/grafana-email" \
      org.opencontainers.image.source="https://gitlab.com/ix.ai/grafana-email"

COPY grafana-email.sh /usr/local/bin/grafana-email.sh
COPY grafana-email/ /grafana-email
RUN set -xeu; \
    apk --no-cache add python3 py3-pillow py3-requests py3-pip; \
    pip install --no-cache-dir --break-system-packages -r grafana-email/requirements.txt

ENTRYPOINT ["/usr/local/bin/grafana-email.sh"]
