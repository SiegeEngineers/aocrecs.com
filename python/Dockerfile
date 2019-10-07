FROM alpine
EXPOSE 3000
VOLUME /usr/src/app/public
WORKDIR /usr/src/app
RUN apk add --no-cache \
        uwsgi-python3 \
        python3 \
        python3-dev \
        build-base \
        linux-headers \
        postgresql-dev
COPY . .
RUN rm -rf public/*
RUN pip3 install --no-cache-dir -e .
CMD ["uwsgi", "--socket", "0.0.0.0:3000", \
              "--uid", "uwsgi", \
              "--plugins", "python3", \
              "--protocol", "uwsgi", \
              "--route-run", "fixpathinfo:", \
              "--wsgi", "wsgi:app"]
