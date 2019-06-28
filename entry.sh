#!/bin/sh

# start cron
set -e

echo "*/5 * * * * /code/launcher.sh >> ~/cron.log 2>&1" | crontab - && crond -f
 