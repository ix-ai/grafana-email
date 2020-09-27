#!/usr/bin/env sh

echo "Setting VERSION='${CI_COMMIT_REF_NAME}-${CI_COMMIT_SHORT_SHA}' in grafana-email/constants.py"
echo "VERSION = '${CI_COMMIT_REF_NAME}-${CI_COMMIT_SHORT_SHA}'" >> grafana-email/constants.py
