# grafana-email

[![Pipeline Status](https://gitlab.com/ix.ai/grafana-email/badges/master/pipeline.svg)](https://gitlab.com/ix.ai/grafana-email/)
[![Docker Stars](https://img.shields.io/docker/stars/ixdotai/grafana-email.svg)](https://hub.docker.com/r/ixdotai/grafana-email/)
[![Docker Pulls](https://img.shields.io/docker/pulls/ixdotai/grafana-email.svg)](https://hub.docker.com/r/ixdotai/grafana-email/)
[![Docker Image Version (latest)](https://img.shields.io/docker/v/ixdotai/grafana-email/latest)](https://hub.docker.com/r/ixdotai/grafana-email/)
[![Docker Image Size (latest)](https://img.shields.io/docker/image-size/ixdotai/grafana-email/latest)](https://hub.docker.com/r/ixdotai/grafana-email/)
[![Gitlab Project](https://img.shields.io/badge/GitLab-Project-554488.svg)](https://gitlab.com/ix.ai/grafana-email/)

Connects to Grafana and sends an e-mail with attached graphs.

> **Warning!** For grafana-email to work, you need the [grafana-image-renderer](https://grafana.com/grafana/plugins/grafana-image-renderer) plugin (details also here: [Image Rendering](https://grafana.com/docs/grafana/latest/administration/image_rendering/)). I'm using the docker image [grafana/grafana-image-renderer](https://hub.docker.com/r/grafana/grafana-image-renderer) for this. See below the example under [Grafana configuration on docker swarm, with grafana-image-renderer](#grafana-configuration-on-docker-swarm-with-grafana-image-renderer)

## Supported environment variables
Example panel url:
```
http://grafana1:3001/render/d-solo/gV6maGVZz/e-mail-reports?orgId=1&from=1562006810978&to=1562078810980&panelId=2&width=1000&height=500&tz=Europe%2FOslo
```

You can see the panel url by selecting `Share` in a panel menu (click on its name) -> `Link` -> `Direct link rendered image`


| **Variable**          | **Default**            | **Mandatory** | **Description**                                                        |
|:----------------------|:----------------------:|:-------------:|:-----------------------------------------------------------------------|
| `GRAFANA_TOKEN`       | -                      | **YES**       | the authentication token for Grafana |
| `GRAFANA_DASHBOARD`   | -                      | **YES**       | the short code for the dashboard (example: **`gV6maGVZz/e-mail-reports`**) |
| `SMTP_FROM`           | -                      | **YES**       | the e-mail address of the sender |
| `SMTP_TO`             | -                      | **YES**       | the e-mail address of the receipient |
| `SMTP_PORT`           | `25`                   | NO            | the port for the SMTP host |
| `SMTP_HOST`           | `localhost`            | NO            | the SMTP host |
| `SMTP_SUBJECT`        | `Grafana Email Report` | NO            | the e-mail subject |
| `PANEL_IDS`           | `1`                    | NO            | comma separated list with the IDs of the panels (example: `2`) |
| `PANEL_ORG_ID`        | `1`                    | NO            | the Grafana organization (in example: `1`) |
| `PANEL_FROM`          | `now-1d`               | NO            | the start of the panel time interval (example: `1562006810978`) |
| `PANEL_TO`            | `now`                  | NO            | the end of the panel time interval (example: `1562078810980`) |
| `PANEL_WIDTH`         | `500`                  | NO            | the width of the image in pixels (example: `1000`) |
| `PANEL_HEIGHT`        | `250`                  | NO            | the height of the image in pixels (example: `500`) |
| `PANEL_THEME`         | `light`                | NO            | one of `dark`, `light` |
| `GRAFANA_HOST`        | `grafana`              | NO            | the hostname or FQDN of the Grafana host (example: `grafana1`) |
| `GRAFANA_PORT`        | `3000`                 | NO            | the port for the Grafana host (example: `3001`) |
| `GELF_PORT`           | `12201`                | NO            | if `GELF_HOST` is configured (see below), use this **UDP** port for logging |
| `LOGLEVEL`            | `INFO`                 | NO            | [Logging Level](https://docs.python.org/3/library/logging.html#levels) |
| `GELF_HOST`           | -                      | NO            | the GELF capable host, for logging |
| `SMTP_USER`           | -                      | NO            | fill this out, if your SMTP server requires authentication |
| `SMTP_PASSWORD`       | -                      | NO            | fill this out, if your SMTP server requires authentication |
| `PANEL_TZ`            | -                      | NO            | the timezone, needed for timestamp `PANEL_FROM` or `PANEL_TO` (example: `Europe/Oslo`) |
| `PANEL_TIMEOUT`       | -                      | NO            | the timeout for Grafana to generate the panel |
| `GRAFANA_HEADER_HOST` | -                      | NO            | useful if the hostname of the Grafana host/container is set to something than the FQDN in Grafana |
| `GRAFANA_URL_PARAMS`  | -                      | NO            | add additional URL params (example: `var-RequestHost=alex&var-Filters=OriginStatus\|!%3D\|404`) |
| `GRAFANA_SSL_VERIFY`  | TRUE                   | NO            | set to `FALSE` to ignore SSL certificate errors |

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
  registry.gitlab.com/ix.ai/grafana-email:latest
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

### Grafana configuration on docker swarm, with grafana-image-renderer
```yml
version: '3.7'

services:
  grafana:
    image: grafana/grafana:latest
    environment:
      GF_INSTALL_PLUGINS: grafana-image-renderer
      GF_LOG_FILTERS: rendering:debug
      GF_RENDERING_SERVER_URL: http://grafana-image-renderer:8081/render
      GF_RENDERING_CALLBACK_URL: http://grafana:3000/
  grafana-image-renderer:
    image: grafana/grafana-image-renderer:latest
    networks:
      - grafana-email
    environment:
      ENABLE_METRICS: 'true'
      LOG_LEVEL: 'info'
```

## Tags and Arch

Starting with version v0.3.0, the images are multi-arch, with builds for amd64, arm64 and armv7. Version v0.4.0 also
adds 386 build.

* `vN.N.N` - for example v0.3.0
* `latest` - always pointing to the latest version
* `dev-master` - the last build on the master branch

## Resources:
* GitLab: https://gitlab.com/ix.ai/grafana-email
* GitHub: https://github.com/ix-ai/grafana-email
* GitLab Registry: https://gitlab.com/ix.ai/grafana-email/container_registry
* Docker Hub: https://hub.docker.com/r/ixdotai/grafana-email
