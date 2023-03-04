FROM alpine
WORKDIR /opt/cybercoin/
COPY cybercoin ./cybercoin
COPY app.py .
COPY config.py .
COPY manage.sh .
RUN apk add python3 py3-pip py3-gunicorn curl
RUN pip3 install flask pycryptodome urllib3 gevent\>=1.4
EXPOSE 8000
CMD ["./manage.sh", "start"]
