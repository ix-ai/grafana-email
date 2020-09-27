FROM alpine:latest
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/grafana-email"

WORKDIR /grafana-email
COPY grafana-email/ /grafana-email
RUN set -xeu; \
    apk --no-cache add python3 py3-pillow py3-requests py3-pip; \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "/grafana-email/grafana-email.py"]
