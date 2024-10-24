FROM alpine:latest@sha256:beefdbd8a1da6d2915566fde36db9db0b524eb737fc57cd1367effd16dc0d06d
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/grafana-email" \
      org.opencontainers.image.source="https://gitlab.com/ix.ai/grafana-email"

COPY grafana-email.sh /usr/local/bin/grafana-email.sh
COPY grafana-email/ /grafana-email
RUN set -xeu; \
    apk --no-cache add python3 py3-pillow py3-requests py3-pip; \
    pip install --no-cache-dir --break-system-packages -r grafana-email/requirements.txt

ENTRYPOINT ["/usr/local/bin/grafana-email.sh"]
