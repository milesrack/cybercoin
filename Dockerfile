FROM alpine
RUN mkdir /opt/cybercoin/
WORKDIR /opt/cybercoin
COPY cybercoin ./cybercoin
COPY app.py .
COPY config.json .
COPY manage.sh .
COPY setup.py .
RUN apk add python3 py3-pip py3-gunicorn curl jq
RUN pip3 install flask pycryptodome urllib3 gevent>=1.4
EXPOSE 8000
CMD ["./manage.sh", "start"]
