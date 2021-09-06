FROM alpine:latest
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/grafana-email"

COPY grafana-email.sh /usr/local/bin/grafana-email.sh
COPY grafana-email/ /grafana-email
RUN set -xeu; \
    apk --no-cache add python3 py3-pillow py3-requests py3-pip; \
    pip install --no-cache-dir -r grafana-email/requirements.txt

ENTRYPOINT ["/usr/local/bin/grafana-email.sh"]
