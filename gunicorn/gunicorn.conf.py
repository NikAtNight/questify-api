# gunicorn.conf.py

# The module path to the WSGI application callable
wsgi_app = "app.wsgi:application"

# Server socket
bind = "0.0.0.0:8000"

# Workers and concurrency
workers = 1               # Number of worker processes. Adjust based on your server's CPU count
worker_class = "sync"      # Type of workers (sync, gevent, eventlet, etc.)
threads = 1                # Number of threads per worker (if using threaded workers)
timeout = 30               # Workers silent for more than this many seconds are killed and restarted

# Logging
accesslog = "-"            # Log access requests (use "-" for stdout)
errorlog = "-"             # Log errors (use "-" for stderr)
loglevel = "info"          # Log level (debug, info, warning, error, critical)

# Graceful shutdown settings
graceful_timeout = 30      # Timeout for graceful workers restart
max_requests = 1000        # Restart workers after this many requests
max_requests_jitter = 50   # Randomize the restart to avoid all workers restarting at once

# Security
limit_request_line = 4094  # Limit the size of HTTP request lines
limit_request_field_size = 8190  # Limit the size of HTTP request headers

# Process naming
proc_name = "gunicorn_app"  # Process name

# Preload app for faster worker startup
preload_app = True
