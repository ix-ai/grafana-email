#!/usr/bin/env python3
""" Connects to Grafana and retrieves the panels, which are then sent per Email """

import logging
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from io import BytesIO
import requests
from PIL import Image
import pygelf
import constants


LOG = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOGLEVEL", "INFO"),
    format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

FILENAME = os.path.splitext(sys.modules['__main__'].__file__)[0]


def configure_logging():
    """ Configures the logging """
    if os.environ.get('GELF_HOST'):
        GELF = pygelf.GelfUdpHandler(
            host=os.environ.get('GELF_HOST'),
            port=int(os.environ.get('GELF_PORT', 12201)),
            debug=True,
            include_extra_fields=True,
            _ix_id=FILENAME
        )
        LOG.addHandler(GELF)
        LOG.info('Initialized logging with GELF enabled')


class GrafanaEmail:
    """ Connects to grafana, downloads graphs, sends them in an email """
    panel_args = {}
    smtp = {}
    grafana = {}
    panels = []

    def __init__(self):
        self.message = MIMEMultipart('related')

        # These are mandatory
        self.smtp['from'] = os.environ['SMTP_FROM']
        self.smtp['to'] = os.environ['SMTP_TO']
        self._token = os.environ['GRAFANA_TOKEN']
        self.grafana['dashboard'] = os.environ['GRAFANA_DASHBOARD']  # Example: gV6maGVZz

        # These are not or have defaults
        self.smtp['port'] = int(os.environ.get('SMTP_PORT', 25))
        self.smtp['host'] = os.environ.get('SMTP_HOST', 'localhost')
        self._smtp_user = os.environ.get('SMTP_USER')
        self._smtp_password = os.environ.get('SMTP_PASSWORD')
        self.grafana['ssl'] = os.environ.get('GRAFANA_SSL')
        self.grafana['host'] = os.environ.get('GRAFANA_HOST', 'grafana')
        self.grafana['header_host'] = os.environ.get('GRAFANA_HEADER_HOST')
        self.grafana['port'] = int(os.environ.get('GRAFANA_PORT', 3000))
        self.grafana['panel_ids'] = os.environ.get('PANEL_IDS', '1')
        self.grafana['url_params'] = os.environ.get('GRAFANA_URL_PARAMS')

        self.panel_args['orgId'] = os.environ.get('PANEL_ORG_ID', '1')
        self.panel_args['timeout'] = int(os.environ.get('PANEL_TIMEOUT', '5'))
        self.panel_args['from'] = os.environ.get('PANEL_FROM', 'now-7d')
        self.panel_args['to'] = os.environ.get('PANEL_TO', 'now')
        self.panel_args['width'] = int(os.environ.get('PANEL_WIDTH', '500'))
        self.panel_args['height'] = int(os.environ.get('PANEL_HEIGHT', '250'))
        self.panel_args['theme'] = os.environ.get('PANEL_THEME', 'light')
        self.panel_args['tz'] = os.environ.get('PANEL_TZ')

        self.message['Subject'] = os.environ.get('SMTP_SUBJECT', 'Grafana Email Report')
        self.message['From'] = self.smtp['from']
        self.message['To'] = self.smtp['to']

        LOG.debug(f'Panel options: {self.panel_args}')
        LOG.debug(f'SMTP options: {self.smtp}')
        LOG.debug(f'Grafana options: {self.grafana}')

    def get_panels(self):
        """ downloads each panel and saves it to a variable """

        method = 'http'
        if self.grafana.get('ssl'):
            method = 'https'

        uri = '{method}://{host}:{port}/render/d-solo/{dashboard}'.format(
            method=method,
            host=self.grafana['host'],
            port=self.grafana['port'],
            dashboard=self.grafana['dashboard']
        )

        if self.grafana.get('url_params'):
            uri = f'{uri}?{self.grafana["url_params"]}'

        LOG.info(f'Setting download URI to {uri}')

        params = {}
        for param, arg in self.panel_args.items():
            if arg:
                params.update({param: arg})

        headers = {'Authorization': f'Bearer {self._token}'}
        if self.grafana.get('header_host'):
            headers.update({'Host': f"{self.grafana['header_host']}"})

        for panel in self.grafana['panel_ids'].split(','):
            params['panelId'] = panel

            response = requests.get(uri, params=params, headers=headers, stream=True)
            response.raw.decode_content = True
            if response:
                # self.panels.append({panel: base64.b64encode(imgObj).decode('UTF-8')})
                self.panels.append({panel: self.transform_image(response.raw)})

    def transform_image(self, image):
        """ takes the binary http answer and transforms it to image object for attaching """
        img = Image.open(image)
        stream = BytesIO()
        img.save(stream, format="png")
        stream.seek(0)
        return stream.read()

    def send_email(self):
        """ sends the email with the embedded panels """
        html = '<html><body><p>'
        host = self.grafana['host']

        for panel, image in [(k, v) for x in self.panels for (k, v) in x.items()]:
            width = str(self.panel_args['width'])
            height = str(self.panel_args['height'])
            html += (
                f'<img src="cid:{host}_panel_{panel}.png"'
                f' style="{{width:{width}px;height:{height}px;padding:10px}}" />'
            )
        html += '</p></body></html>'

        part = MIMEText(html, "html")
        self.message.attach(part)

        for panel, image in [(k, v) for x in self.panels for (k, v) in x.items()]:
            img = MIMEImage(image, 'png')
            img.add_header('Content-ID', f'<{host}_panel_{panel}.png>')
            img.add_header(
                'Content-Disposition',
                'inline',
                filename=f'{host}_panel_{panel}.png',
            )
            self.message.attach(img)

        # send your email
        with smtplib.SMTP(self.smtp['host'], self.smtp['port']) as server:
            if self.smtp.get('user') and self.smtp.get('password'):
                server.login(self._smtp_user, self._smtp_password)
            if self.panels:  # Only send if there are panels
                server.sendmail(
                    self.smtp['from'],
                    self.smtp['to'],
                    self.message.as_string()
                )
                server.quit()
            else:
                LOG.error('Panels not downloaded. No e-mail sent.')
        LOG.info('Sent')


if __name__ == '__main__':
    configure_logging()
    # pylint: disable=no-member
    LOG.info(f"Starting {FILENAME} {constants.VERSION}")
    grafana = GrafanaEmail()
    grafana.get_panels()
    grafana.send_email()
