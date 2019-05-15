#!/bin/bash

function postgres_ready(){
python << END
import sys
import psycopg2
import environ
try:
    ROOT_DIR = environ.Path(__file__) - 3
    APPS_DIR = ROOT_DIR.path('src')
    ENV_PATH = str(APPS_DIR.path('.env'))
    env = environ.Env()
    if env.bool('READ_ENVFILE', default=True):
        env.read_env(ENV_PATH)
    conn = psycopg2.connect(dbname=env('POSTGRES_DB', default=''), user=env('POSTGRES_USER', default=''), password=env('POSTGRES_PASSWORD', default=''), host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

# migrate any changes to the database container
python /src/manage.py migrate --noinput
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

# load data if LOAD_DATA is on
if [ "x$LOAD_DATA" = 'xon' ]; then
    python /src/manage.py loaddata /src/fixtures/*.json
fi

# collect static files
find . -name '*.pyc' -delete && \
  python /src/manage.py collectstatic --noinput

uwsgi --http-auto-chunked --http-keepalive --static-map /static=/src/assets --static-map /media=/src/media
