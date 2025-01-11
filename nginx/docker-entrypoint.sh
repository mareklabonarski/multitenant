#!/bin/bash
###########

sh -c "/entrypoint/nginxReloader.sh &"
exec "$@"
