import multiprocessing
import os

# Bind to Render's dynamic port
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")

# Workers (optimized)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker type
worker_class = "sync"

# Timeout
timeout = 120

# Keep alive
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"

# Stability
max_requests = 1000
max_requests_jitter = 100
