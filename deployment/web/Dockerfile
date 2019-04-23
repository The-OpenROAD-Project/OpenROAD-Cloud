FROM python:3.5

ENV PYTHONUNBUFFERED 1

COPY deployment/requirements.deploy.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY src /src/
COPY deployment/web/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

WORKDIR /src

RUN mkdir media && chmod 777 media && \
    mkdir static && chmod 777 static && \
    mkdir /designs && chmod 777 /designs && \
    mkdir /validation_tmp && chmod 777 /validation_tmp

ENV DJANGO_SETTINGS_MODULE=flow.settings
ENV UWSGI_WSGI_FILE=/src/flow/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
