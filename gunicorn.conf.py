# Gunicorn configuration for Chidmano Store Analysis
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes - use 1 for Liara to avoid memory issues
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes for AI processing
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'chidmano_store_analysis'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None

# Preload app for better performance
preload_app = True

# Worker timeout for AI processing
worker_timeout = 300  # 5 minutes
graceful_timeout = 120  # 2 minutes for graceful shutdown