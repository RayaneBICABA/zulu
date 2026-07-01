import os

bind = "0.0.0.0:" + os.getenv("PORT", "5000")
workers = int(os.getenv("GUNICORN_WORKERS", "4"))
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "-"
accesslog = "-"
loglevel = "info"
