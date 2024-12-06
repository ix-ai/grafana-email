FROM alpine:latest@sha256:21dc6063fd678b478f57c0e13f47560d0ea4eeba26dfc947b2a4f81f686b9f45
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/grafana-email" \
      org.opencontainers.image.source="https://gitlab.com/ix.ai/grafana-email"

COPY grafana-email.sh /usr/local/bin/grafana-email.sh
COPY grafana-email/ /grafana-email
RUN set -xeu; \
    apk --no-cache add python3 py3-pillow py3-requests py3-pip; \
    pip install --no-cache-dir --break-system-packages -r grafana-email/requirements.txt

ENTRYPOINT ["/usr/local/bin/grafana-email.sh"]
