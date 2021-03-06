#!/bin/bash

set -e
RET=0

pip uninstall -y powerlibs-django-contrib-eventful || echo "Could not uninstall."
pip install -U "git+file://$PWD" --no-cache-dir
mv powerlibs x
PYTHONPATH=. py.test tests/ || RET=$?
mv x powerlibs
exit $RET
