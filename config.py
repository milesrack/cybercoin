registration_node = "http://127.0.0.1:8000/"
private_key = ""

port = "8000"
bind = "0.0.0.0:" + port
wsgi_app = "app:app"
accesslog = "logs/access.log"
errorlog = "logs/error.log"
pidfile = "/tmp/gunicorn.pid"
worker_class = "gevent"
daemon = True
