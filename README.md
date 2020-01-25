# grafana-email

[![Pipeline Status](https://gitlab.com/ix.ai/grafana-email/badges/master/pipeline.svg)](https://gitlab.com/ix.ai/grafana-email/)
[![Docker Stars](https://img.shields.io/docker/stars/ixdotai/grafana-email.svg)](https://hub.docker.com/r/ixdotai/grafana-email/)
[![Docker Pulls](https://img.shields.io/docker/pulls/ixdotai/grafana-email.svg)](https://hub.docker.com/r/ixdotai/grafana-email/)
[![Gitlab Project](https://img.shields.io/badge/GitLab-Project-554488.svg)](https://gitlab.com/ix.ai/grafana-email/)

Connects to Grafana and sends an e-mail with attached graphs.

## Supported environment variables
Example panel url:
```
http://grafana1:3001/render/d-solo/gV6maGVZz/e-mail-reports?orgId=1&from=1562006810978&to=1562078810980&panelId=2&width=1000&height=500&tz=Europe%2FOslo
```

You can see the panel url by selecting `Share` in a panel menu (click on its name) -> `Link` -> `Direct link rendered image`
### Mandatory
* `GRAFANA_TOKEN` (**mandatory** - no default) - the authentication token for Grafana
* `GRAFANA_DASHBOARD` (**mandatory** - no default) - the short code for the dashboard (example: **`gV6maGVZz/e-mail-reports`**)
* `SMTP_FROM` (**mandatory** - no default) - the e-mail address of the sender
* `SMTP_TO` (**mandatory** - no default) - the e-mail address of the receipient

### Optional, with defaults
* `SMTP_PORT` (default: `25`) - the port for the SMTP host
* `SMTP_HOST` (default: `localhost`) - the SMTP host
* `SMTP_SUBJECT` (default: `Grafana Email Report`) - the e-mail subject
* `PANEL_IDS` (default: `1`) - comma separated list with the IDs of the panels (example: `2`)
* `PANEL_ORG_ID` (default: `1`) - the Grafana organization (in example: `1`)
* `PANEL_FROM` (default: `now-1d`) - the start of the panel time interval (example: `1562006810978`)
* `PANEL_TO` (default: `now`) - the end of the panel time interval (example: `1562078810980`)
* `PANEL_WIDTH` (default: `500`) - the width of the image in pixels (example: `1000`)
* `PANEL_HEIGHT` (default: `250`) - the height of the image in pixels (example: `500`)
* `PANEL_THEME` (default: `light`) - one of `dark`, `light`
* `GRAFANA_HOST` (default: `grafana`) - the hostname or FQDN of the Grafana host (example: `grafana1`)
* `GRAFANA_PORT` (default: `3000`) - the port for the Grafana host (example: `3001`)
* `GELF_PORT` (default: `12201`) - if `GELF_HOST` is configured (see below), use this **UDP** port for logging
* `LOGLEVEL` (default: `INFO`)

### Optional, without defaults
* `GELF_HOST` (no default) - the GELF capable host, for logging
* `SMTP_USER` (no default) - fill this out, if your SMTP server requires authentication
* `SMTP_PASSWORD` (no default) - fill this out, if your SMTP server requires authentication
* `PANEL_TZ` (no default) - the timezone, needed for timestamp `PANEL_FROM` or `PANEL_TO` (example: `Europe/Oslo`)
* `PANEL_TIMEOUT` (no default) - the timeout for Grafana to generate the panel
* `GRAFANA_HEADER_HOST` (no default) - useful if the docker hostname of the Grafana container is set to something different from the
* `GRAFANA_URL_PARAMS` (no default) - add additional URL params (example: `var-RequestHost=alex.thom.ae&var-Filters=OriginStatus|!%3D|404`)

## Examples
### Bash
```sh
docker run -it --rm --name=grafana-email \
  -e GRAFANA_TOKEN='MyAmazingTokenFromGrafana=' \
  -e GRAFANA_DASHBOARD="gV6maGVZz/e-mail-reports" \
  -e SMTP_FROM="test-docker@example.com" \
  -e SMTP_TO="grafana@example.com" \
  -e SMTP_HOST="10.0.10.1" \
  -e PANEL_IDS="2,5,6" \
  -e PANEL_FROM="now-6h" \
  -e PANEL_THEME="light" \
  -e PANEL_TZ="Europe/Berlin" \
  -e GRAFANA_HOST="grafana1" \
  -e GRAFANA_PORT="3001" \
  -e GELF_HOST="graylog" \
  -e GRAFANA_HEADER_HOST="grafana.example.com" \
  -e LOGLEVEL="DEBUG" \
  ixdotai/grafana-email:latest
```

### systemd example:
Place the files under `/etc/systemd/system` and run `sudo systemctl daemon-reload`. You can test it by running
`sudo systemctl start grafana-email.service --now`.
#### grafana-email.service
```
[Unit]
Description=Send an e-mail with Grafana graphs
After=docker.service

[Service]
Type=oneshot
ExecStart=docker run -it --rm --name=grafana-email \
-e GRAFANA_TOKEN='MyAmazingTokenFromGrafana=' \
-e GRAFANA_DASHBOARD="gV6maGVZz/e-mail-reports" \
-e SMTP_FROM="test-docker@example.com" \
-e SMTP_TO="grafana@example.com" \
-e SMTP_HOST="10.0.10.1" \
-e PANEL_IDS="2,5,6" \
-e PANEL_FROM="now-6h" \
-e PANEL_THEME="light" \
-e PANEL_TZ="Europe/Berlin" \
-e GRAFANA_HOST="grafana1" \
-e GRAFANA_PORT="3001" \
-e GELF_HOST="graylog" \
-e GRAFANA_HEADER_HOST="grafana.example.com" \
-e LOGLEVEL="DEBUG" \
registry.gitlab.com/ix.ai/grafana-email:latest
```
#### grafana-email.timer
```
[Unit]
Description=Timer for grafana-email.service daily at 06:59

[Timer]
OnCalendar=06:59

[Install]
WantedBy=multi-user.target
```

## Resources:
* GitLab: https://gitlab.com/ix.ai/grafana-email
* GitHub: https://github.com/ix-ai/grafana-email
* Docker Hub: https://hub.docker.com/r/ixdotai/grafana-email
