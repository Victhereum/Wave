#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


# python /app/manage.py collectstatic --noinput

# compress_enabled() {
# python << END
# import sys

# from environ import Env

# env = Env(COMPRESS_ENABLED=(bool, True))
# if env('COMPRESS_ENABLED'):
#     sys.exit(0)
# else:
#     sys.exit(1)

# END
# }

# if compress_enabled; then
#   # NOTE this command will fail if django-compressor is disabled
#   python /app/manage.py compress
# fi
# exec /usr/local/bin/gunicorn config.asgi --bind 0.0.0.0:5000 --chdir=/app -k uvicorn.workers.UvicornWorker

# apt-get update && \
#     apt-get install -y ffmpeg

pip install -r requirements/production.txt

python manage.py collectstatic --noinput
python manage.py compress

python manage.py spectacular --color --file schema.yml
python manage.py migrate
exec /usr/local/bin/gunicorn config.asgi --bind 0.0.0.0:5000 --chdir=/app -k uvicorn.workers.UvicornWorker
