FROM flask-base
# RUN apk add make postgresql-dev musl-dev gcc g++ python3-dev zlib-dev libffi-dev && rm -rf /var/cache/apk/*

ENV PYTHONUNBUFFERED=1
ARG flask_port=80
ENV FLASK_RUN_PORT=5000
EXPOSE 3000
EXPOSE 3001
EXPOSE $FLASK_RUN_PORT


WORKDIR /usr/src/app
ADD . .

# RUN python3 -m pip install -r requirements.txt --no-cache-dir
WORKDIR /usr/src/app/src
CMD gunicorn -k gevent -w 2 --bind 0.0.0.0:${FLASK_RUN_PORT} app:app
