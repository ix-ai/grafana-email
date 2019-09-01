FROM alpine:latest

LABEL maintainer="docker@ix.ai"

WORKDIR /app

COPY src/ /app

RUN apk --no-cache add python3 && \
    pip3 install --no-cache-dir -r requirements.txt

ENV SMTP_PORT=25 SMTP_HOST=localhost SMTP_SUBJECT="Grafana Email Report"
ENV PANEL_IDS=1 PANEL_ORG_ID=1 PANEL_FROM=now-1d PANEL_TO=now PANEL_TIMEOUT=30 PANEL_WIDTH=500 PANEL_HEIGHT=250 PANEL_THEME=light
ENV GRAFANA_HOST=grafana GRAFANA_PORT=3000
ENV LOGLEVEL=INFO GELF_PORT=12201

ENTRYPOINT ["python3", "/app/grafana-email.py"]
