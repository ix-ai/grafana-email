FROM alpine:latest@sha256:1e42bbe2508154c9126d48c2b8a75420c3544343bf86fd041fb7527e017a4b4a
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/grafana-email" \
      org.opencontainers.image.source="https://gitlab.com/ix.ai/grafana-email"

COPY grafana-email.sh /usr/local/bin/grafana-email.sh
COPY grafana-email/ /grafana-email
RUN set -xeu; \
    apk --no-cache add python3 py3-pillow py3-requests py3-pip; \
    pip install --no-cache-dir --break-system-packages -r grafana-email/requirements.txt

ENTRYPOINT ["/usr/local/bin/grafana-email.sh"]
